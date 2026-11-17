"""
============================================================================
SkillBridge AI - Web Server
============================================================================
Run:   python3 server.py
Open:  http://localhost:8010

Serves the website and a JSON API. Runs on Python's standard library alone
(offline rule-based AI). With `pip install -r requirements.txt` and an
ANTHROPIC_API_KEY set, the AI Mentor and interview grading use Claude.

Auth
  POST /api/register            { full_name, email, password }
  POST /api/login               { email, password }
  POST /api/logout
  GET  /api/me
Career data (login required)
  GET  /api/catalog             roles, skills and level names
  GET  /api/profile             POST /api/profile { target_role, current_status, hours_per_week, skills }
  GET  /api/dashboard           readiness, next task, stats, activity
  GET  /api/analysis            skill-gap analysis for the target role
  GET  /api/roadmap             personalized week-by-week roadmap
  POST /api/progress            { task_id, done }
  POST /api/resume              { text, apply }   -> resume score & skills found
  GET  /api/interview?focus=id  question set
  POST /api/interview/evaluate  { question_id, answer } -> score, feedback, source
  GET  /api/jobs                POST /api/jobs/save { job_id, saved }
  POST /api/mentor              { message, history }  -> { reply, source }
============================================================================
"""

import json
import os
import re
from http import cookies
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env_file(path=os.path.join(ROOT_DIR, ".env")):
    """Read KEY=value lines from .env (e.g. ANTHROPIC_API_KEY) without overriding real env vars."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            key, sep, value = line.strip().partition("=")
            if sep and key and not key.startswith("#"):
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()  # before importing llm, which reads the environment

from database import db  # noqa: E402
from engine import ai, llm  # noqa: E402
from engine.knowledge import JOBS, LEVEL_NAMES, ROLES, SKILLS  # noqa: E402

PORT = int(os.environ.get("PORT", 8010))
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")
COOKIE_NAME = "sb_session"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_BODY = 60_000
STATUSES = ["Student", "Fresh graduate", "Working professional", "Career switcher"]


class SkillBridgeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    # ----- helpers ---------------------------------------------------------
    def send_json(self, status, data, extra_headers=None):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for name, value in (extra_headers or []):
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0 or length > MAX_BODY:
            return {}
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            return data if isinstance(data, dict) else {}
        except (ValueError, UnicodeDecodeError):
            return {}

    def get_session_token(self):
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        return jar[COOKIE_NAME].value if COOKIE_NAME in jar else None

    def session_cookie(self, token, max_age):
        return ("Set-Cookie", f"{COOKIE_NAME}={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={max_age}")

    def current_user(self):
        user = db.get_user_by_session(self.get_session_token())
        if not user:
            self.send_json(401, {"error": "Please log in."})
        return user

    def user_state(self, user):
        return db.get_profile(user["id"]), db.get_completed(user["id"])

    def log_message(self, fmt, *args):
        if "/api/" in str(args[0] if args else "") or fmt.startswith("code"):
            super().log_message(fmt, *args)

    # ----- GET -------------------------------------------------------------
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path

        if not path.startswith("/api/"):
            if path in ("/", ""):
                self.path = "/index.html"
            elif "." not in path.rsplit("/", 1)[-1]:
                self.path = path + ".html"
            return super().do_GET()

        if path == "/api/catalog":
            return self.send_json(200, {
                "roles": [{"id": k, "title": r["title"], "icon": r["icon"], "summary": r["summary"],
                           "skills": list(r["skills"].keys())} for k, r in ROLES.items()],
                "skills": [{"id": k, "name": s["name"], "category": s["category"]} for k, s in SKILLS.items()],
                "levels": LEVEL_NAMES, "statuses": STATUSES,
                "ai": llm.status(),
            })

        user = self.current_user()
        if not user:
            return
        profile, completed = self.user_state(user)

        if path == "/api/me":
            return self.send_json(200, {"user": {"id": user["id"], "full_name": user["full_name"],
                                                 "email": user["email"]}, "profile": profile})
        if path == "/api/profile":
            return self.send_json(200, profile)
        if path == "/api/analysis":
            return self.send_json(200, ai.analyze(profile, completed))
        if path == "/api/roadmap":
            return self.send_json(200, ai.build_roadmap(profile, completed))
        if path == "/api/interview":
            focus = parse_qs(url.query).get("focus", [None])[0]
            return self.send_json(200, {"questions": ai.interview_set(profile, completed, focus)})
        if path == "/api/jobs":
            saved = db.get_saved_jobs(user["id"])
            jobs = [{**j, "saved": j["id"] in saved} for j in ai.match_jobs(profile, completed)]
            return self.send_json(200, {"jobs": jobs})
        if path == "/api/dashboard":
            report = ai.analyze(profile, completed)
            roadmap = ai.build_roadmap(profile, completed)
            jobs = ai.match_jobs(profile, completed)
            return self.send_json(200, {
                "name": user["full_name"], "profile": profile,
                "readiness": report["readiness"], "verdict": report["verdict"],
                "role": report["role"], "icon": report["icon"],
                "skills": report["skills"], "hours_left": report["hours_left"],
                "weeks_left": report["weeks_left"],
                "roadmap": {k: roadmap[k] for k in ("percent", "done_tasks", "total_tasks", "next_task")},
                "top_jobs": jobs[:3],
                "jobs_ready": sum(1 for j in jobs if j["match"] >= 75),
                "stats": db.activity_stats(user["id"]),
                "activity": db.recent_activity(user["id"]),
            })
        self.send_json(404, {"error": "Not found"})

    # ----- POST ------------------------------------------------------------
    def do_POST(self):
        path = urlparse(self.path).path
        data = self.read_json()

        if path == "/api/register":
            name = str(data.get("full_name", "")).strip()
            email = str(data.get("email", "")).strip()
            password = str(data.get("password", ""))
            if len(name) < 2:
                return self.send_json(400, {"error": "Please enter your full name."})
            if not EMAIL_PATTERN.match(email):
                return self.send_json(400, {"error": "Please enter a valid email address."})
            if len(password) < 8:
                return self.send_json(400, {"error": "Password must be at least 8 characters."})
            user_id = db.create_user(name, email, password)
            if not user_id:
                return self.send_json(409, {"error": "An account with this email already exists."})
            token = db.create_session(user_id)
            return self.send_json(201, {"ok": True},
                                  [self.session_cookie(token, db.SESSION_DAYS * 86400)])

        if path == "/api/login":
            user = db.authenticate(str(data.get("email", "")).strip(), str(data.get("password", "")))
            if not user:
                return self.send_json(401, {"error": "Incorrect email or password."})
            token = db.create_session(user["id"])
            return self.send_json(200, {"ok": True}, [self.session_cookie(token, db.SESSION_DAYS * 86400)])

        if path == "/api/logout":
            db.delete_session(self.get_session_token())
            return self.send_json(200, {"ok": True}, [self.session_cookie("", 0)])

        user = self.current_user()
        if not user:
            return
        profile, completed = self.user_state(user)

        if path == "/api/profile":
            role = data.get("target_role")
            if role not in ROLES:
                return self.send_json(400, {"error": "Please choose a target role."})
            status = data.get("current_status") if data.get("current_status") in STATUSES else "Student"
            try:
                hours = min(max(int(data.get("hours_per_week", 8)), 1), 60)
            except (TypeError, ValueError):
                hours = 8
            skills = {}
            for skill_id, level in (data.get("skills") or {}).items():
                if skill_id in SKILLS and isinstance(level, int) and 1 <= level <= 5:
                    skills[skill_id] = level
            db.save_profile(user["id"], role, status, hours, skills)
            return self.send_json(200, {"ok": True})

        if path == "/api/progress":
            task_id = str(data.get("task_id", ""))
            if task_id not in ai.valid_task_ids(profile):
                return self.send_json(400, {"error": "Unknown task."})
            db.set_task(user["id"], task_id, bool(data.get("done")))
            if data.get("done"):
                db.log_activity(user["id"], "task", task_id)
            return self.send_json(200, ai.build_roadmap(profile, db.get_completed(user["id"])))

        if path == "/api/resume":
            text = str(data.get("text", ""))
            if len(text.split()) < 30:
                return self.send_json(400, {"error": "Please paste your full resume (at least 30 words)."})
            result = ai.analyze_resume(text, profile["target_role"])
            db.log_activity(user["id"], "resume", "Resume scan", result["score"])
            if data.get("apply"):
                skills = dict(profile["skills"])
                for s in result["skills_found"]:
                    skills[s["id"]] = max(skills.get(s["id"], 0), s["suggested_level"])
                db.save_profile(user["id"], profile["target_role"], profile["current_status"],
                                profile["hours_per_week"], skills)
                result["applied"] = True
            return self.send_json(200, result)

        if path == "/api/interview/evaluate":
            qid = str(data.get("question_id", ""))
            answer = str(data.get("answer", ""))[:5000]
            q = ai.get_question(qid)
            if not q:
                return self.send_json(400, {"error": "Unknown question."})
            result = None
            if len(answer.split()) >= 8:  # don't spend a Claude call on an empty answer
                result = llm.grade_answer(q, role_title(profile), answer)
            if result:
                result["tip"] = q["tip"]
                result["source"] = "claude"
            else:
                result = {**ai.evaluate_answer(qid, answer), "source": "local"}
            db.log_activity(user["id"], "interview", f"{q['skill']}: {q['question'][:60]}", result["score"])
            return self.send_json(200, result)

        if path == "/api/jobs/save":
            job_id = data.get("job_id")
            if job_id not in {j["id"] for j in JOBS}:
                return self.send_json(400, {"error": "Unknown job."})
            db.set_saved_job(user["id"], job_id, bool(data.get("saved")))
            return self.send_json(200, {"ok": True})

        if path == "/api/mentor":
            message = str(data.get("message", "")).strip()[:1000]
            if not message:
                return self.send_json(400, {"error": "Please type a message."})
            history = data.get("history") if isinstance(data.get("history"), list) else []
            reply = None
            if llm.enabled():
                reply = llm.mentor_reply(message, history, mentor_context(user, profile, completed))
            if reply:
                return self.send_json(200, {"reply": reply, "source": "claude"})
            reply = ai.mentor_reply(message, profile, completed, user["full_name"])
            return self.send_json(200, {"reply": reply, "source": "local"})

        self.send_json(404, {"error": "Not found"})


def role_title(profile):
    return ai.role_or_default(profile.get("target_role"))["title"]


def mentor_context(user, profile, completed):
    report = ai.analyze(profile, completed)
    resources = {g["name"]: SKILLS[g["id"]]["resources"] for g in report["gaps"][:5]}
    return llm.learner_context(user["full_name"], report, ai.build_roadmap(profile, completed),
                               ai.match_jobs(profile, completed), resources)


def main():
    db.init_db()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), SkillBridgeHandler)
    print(f"SkillBridge AI running at http://localhost:{PORT}", flush=True)
    ai_status = llm.status()
    print(f"AI engine: Claude ({ai_status['model']})" if ai_status["enabled"]
          else f"AI engine: offline rule-based ({ai_status['reason']})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
