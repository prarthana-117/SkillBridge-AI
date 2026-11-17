-- ==========================================================================
-- SkillBridge AI - SQLite schema
-- ==========================================================================

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,          -- pbkdf2_sha256$iterations$salt$hash
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS sessions (
    token      TEXT    PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TEXT    NOT NULL
);

-- One career profile per user: target role, self-rated skills, study time.
CREATE TABLE IF NOT EXISTS profiles (
    user_id        INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    target_role    TEXT    NOT NULL DEFAULT 'fullstack',
    current_status TEXT    NOT NULL DEFAULT 'Student',
    hours_per_week INTEGER NOT NULL DEFAULT 8,
    skills_json    TEXT    NOT NULL DEFAULT '{}',   -- {"python": 3, "sql": 2}
    updated_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Roadmap tasks the user has ticked off.
CREATE TABLE IF NOT EXISTS completed_tasks (
    user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id      TEXT    NOT NULL,
    completed_at TEXT    NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, task_id)
);

-- History of resume scans and interview answers (for the progress chart).
CREATE TABLE IF NOT EXISTS activity (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind       TEXT    NOT NULL,                     -- resume | interview | task
    label      TEXT    NOT NULL,
    score      INTEGER,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Jobs the user bookmarked.
CREATE TABLE IF NOT EXISTS saved_jobs (
    user_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id   INTEGER NOT NULL,
    saved_at TEXT    NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, job_id)
);
