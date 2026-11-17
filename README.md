# SkillBridge AI

An AI career co-pilot that bridges the gap between the skills you have and the job you want.

## Run it

**Easiest (macOS):** double-click `Start SkillBridge.command`. The first run installs the Claude SDK and
creates a `.env` file — paste your key after `ANTHROPIC_API_KEY=` in `.env` and start it again to turn on Claude.

**Manually:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # optional - enables Claude
.venv/bin/python server.py
```

Open http://localhost:8010. The SQLite database (`database/skillbridge.db`) is created on first run.
The startup log says which AI engine is active.

### AI engine: Claude or offline

| Setup | AI Mentor | Interview grading |
| --- | --- | --- |
| SDK installed + `ANTHROPIC_API_KEY` set | Claude answers using the learner's full profile, gaps, roadmap and job matches, with conversation memory | Claude grades the answer, lists covered/missing points, gives coaching and a sample strong answer |
| No key, or no SDK (`python3 server.py` works with zero installs) | Rule-based intent replies | Keyword-coverage scoring |

If a Claude call fails (bad key, rate limit, network), that request silently falls back to the offline engine,
so the site never breaks. Errors are logged to the server console.

- Model: `claude-opus-5-5` (override with `SKILLBRIDGE_MODEL`). Mentor runs at `low` effort for fast replies; grading at `medium`
  with a JSON schema so results are always well-formed.
- Server-side refusal fallback is enabled (`fallbacks: "default"`): if Claude declines a request, the API retries on
  Anthropic's recommended fallback model inside the same call.
- The UI shows a **Powered by Claude** / **Offline AI mode** badge on the Mentor and Interview Coach pages.

## What it does

| Module | What the user gets |
| --- | --- |
| **Profile & Skills** | Pick one of 10 target roles, set weekly study hours, self-rate 33 skills (1–5). |
| **Skill Gap Analysis** | Weighted readiness score, strong / developing / missing skills, hours and weeks left. |
| **Learning Roadmap** | Week-by-week plan in 4 phases (Foundation → Build → Polish → Career Launch) with learn / practice / project tasks and free official resources. Completing a skill's tasks raises your readiness. |
| **Resume Analyzer** | ATS-style score out of 100 (role keywords, sections, metrics, action verbs, length), detected skills, missing keywords, fixes. One click adds detected skills to your profile. |
| **Interview Coach** | Technical questions for your role (weakest skills first) plus behavioral ones; answers are scored on key-concept coverage, depth and examples. |
| **Job Matches** | Sample openings ranked by match %, showing skills you have vs. need; filter and save jobs. |
| **AI Mentor** | Chat that answers "what next?", "how ready am I?", "how long?", project ideas, skill resources — using your own data. |
| **Dashboard** | Readiness ring, next step, stats, skills-vs-target chart, top jobs, recent activity. |

## Project layout

```
server.py            HTTP server + JSON API (see docstring for routes)
engine/knowledge.py  Skills, roles, resources, interview questions, sample jobs
engine/ai.py         Analysis, roadmap, resume, interview, job matching, offline mentor logic
engine/llm.py        Claude integration (Anthropic SDK): mentor chat + interview grading
database/            SQLite schema and helpers (users, sessions, profiles, progress, activity)
public/              index (landing), login, register, app (dashboard) + css/js
```

To add a role or skill, edit `engine/knowledge.py` — the whole app picks it up.

## Notes

- Passwords are hashed with PBKDF2-SHA256; sessions use HttpOnly cookies.
- Skill-gap analysis, roadmap, resume scoring and job matching are deterministic (knowledge-base driven), so scores are
  consistent and free to compute; Claude handles the open-ended parts (chat and answer grading).
- Job listings are fictional samples for demonstration.
