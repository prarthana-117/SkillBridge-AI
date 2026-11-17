"""
============================================================================
SkillBridge AI - Database helpers (SQLite, standard library only)
============================================================================
"""

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "skillbridge.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")
SESSION_DAYS = 7
PBKDF2_ITERATIONS = 200_000


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with connect() as conn, open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())


# ----- passwords -----------------------------------------------------------
def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PBKDF2_ITERATIONS).hex()
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${digest}"


def verify_password(password, stored):
    try:
        _, iterations, salt, digest = stored.split("$")
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations)).hex()
    return hmac.compare_digest(check, digest)


# ----- users & sessions ----------------------------------------------------
def create_user(full_name, email, password):
    with connect() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (?, ?, ?)",
                (full_name, email.lower(), hash_password(password)))
        except sqlite3.IntegrityError:
            return None
        conn.execute("INSERT INTO profiles (user_id) VALUES (?)", (cur.lastrowid,))
        return cur.lastrowid


def authenticate(email, password):
    with connect() as conn:
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower(),)).fetchone()
    if user and verify_password(password, user["password_hash"]):
        return user
    return None


def create_session(user_id):
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(days=SESSION_DAYS)
    with connect() as conn:
        conn.execute("DELETE FROM sessions WHERE expires_at < ?", (now_iso(),))
        conn.execute("INSERT INTO sessions VALUES (?, ?, ?)", (token, user_id, expires.isoformat()))
    return token


def get_user_by_session(token):
    if not token:
        return None
    with connect() as conn:
        return conn.execute(
            "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id "
            "WHERE s.token = ? AND s.expires_at > ?", (token, now_iso())).fetchone()


def delete_session(token):
    with connect() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


# ----- profile -------------------------------------------------------------
def get_profile(user_id):
    with connect() as conn:
        row = conn.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        return {"target_role": "fullstack", "current_status": "Student", "hours_per_week": 8,
                "skills": {}, "is_new": True}
    return {"target_role": row["target_role"], "current_status": row["current_status"],
            "hours_per_week": row["hours_per_week"], "skills": json.loads(row["skills_json"]),
            "is_new": row["skills_json"] == "{}"}


def save_profile(user_id, target_role, current_status, hours_per_week, skills):
    with connect() as conn:
        conn.execute(
            "INSERT INTO profiles (user_id, target_role, current_status, hours_per_week, skills_json, updated_at) "
            "VALUES (?, ?, ?, ?, ?, datetime('now')) "
            "ON CONFLICT(user_id) DO UPDATE SET target_role = excluded.target_role, "
            "current_status = excluded.current_status, hours_per_week = excluded.hours_per_week, "
            "skills_json = excluded.skills_json, updated_at = excluded.updated_at",
            (user_id, target_role, current_status, hours_per_week, json.dumps(skills)))


# ----- roadmap progress ----------------------------------------------------
def get_completed(user_id):
    with connect() as conn:
        rows = conn.execute("SELECT task_id FROM completed_tasks WHERE user_id = ?", (user_id,))
        return {r["task_id"] for r in rows}


def set_task(user_id, task_id, done):
    with connect() as conn:
        if done:
            conn.execute("INSERT OR IGNORE INTO completed_tasks (user_id, task_id) VALUES (?, ?)",
                         (user_id, task_id))
        else:
            conn.execute("DELETE FROM completed_tasks WHERE user_id = ? AND task_id = ?",
                         (user_id, task_id))


# ----- activity & saved jobs -----------------------------------------------
def log_activity(user_id, kind, label, score=None):
    with connect() as conn:
        conn.execute("INSERT INTO activity (user_id, kind, label, score) VALUES (?, ?, ?, ?)",
                     (user_id, kind, label, score))


def recent_activity(user_id, limit=8):
    with connect() as conn:
        rows = conn.execute("SELECT kind, label, score, created_at FROM activity WHERE user_id = ? "
                            "ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()
    return [dict(r) for r in rows]


def activity_stats(user_id):
    with connect() as conn:
        rows = conn.execute("SELECT kind, COUNT(*) AS n, MAX(score) AS best, "
                            "(SELECT score FROM activity a2 WHERE a2.user_id = a.user_id AND a2.kind = a.kind "
                            " ORDER BY id DESC LIMIT 1) AS last "
                            "FROM activity a WHERE user_id = ? GROUP BY kind", (user_id,)).fetchall()
    return {r["kind"]: {"count": r["n"], "best": r["best"], "last": r["last"]} for r in rows}


def get_saved_jobs(user_id):
    with connect() as conn:
        return {r["job_id"] for r in conn.execute("SELECT job_id FROM saved_jobs WHERE user_id = ?", (user_id,))}


def set_saved_job(user_id, job_id, saved):
    with connect() as conn:
        if saved:
            conn.execute("INSERT OR IGNORE INTO saved_jobs (user_id, job_id) VALUES (?, ?)", (user_id, job_id))
        else:
            conn.execute("DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?", (user_id, job_id))
