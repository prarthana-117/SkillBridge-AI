"""
============================================================================
SkillBridge AI - Engine
============================================================================
The "brain" of SkillBridge. Pure functions that take a user's profile and
return analysis, roadmaps, resume feedback, interview scoring, job matches
and mentor replies. No external services - everything runs locally from
the knowledge base in knowledge.py.
============================================================================
"""

import math
import re

from .knowledge import (BEHAVIORAL_QUESTIONS, JOBS, LEVEL_NAMES, QUESTIONS,
                        ROLES, SKILLS, WEIGHTS)

JOB_READY_LEVEL = 3
CAREER_TASKS = [
    ("career:1", "Update your resume with every new skill and project", 2),
    ("career:2", "Do 3 mock interviews in the Interview Coach", 3),
    ("career:3", "Apply to 5 matching jobs from Job Matches", 3),
]


# ---------------------------------------------------------------------------
# Skill levels and readiness
# ---------------------------------------------------------------------------
def role_or_default(role_id):
    return ROLES.get(role_id) or ROLES["fullstack"]


def task_ids_for_skill(skill_id):
    return [f"{skill_id}:learn", f"{skill_id}:practice", f"{skill_id}:project"]


def effective_levels(profile, completed):
    """Self-rated levels, raised to the role target once a skill's roadmap
    tasks are all completed (that's how learning moves the score)."""
    levels = {k: int(v) for k, v in (profile.get("skills") or {}).items() if k in SKILLS}
    role = role_or_default(profile.get("target_role"))
    for skill_id, (target, _) in role["skills"].items():
        if all(t in completed for t in task_ids_for_skill(skill_id)):
            levels[skill_id] = max(levels.get(skill_id, 0), target)
    return levels


def hours_to_close(skill_id, have, target):
    gap = max(target - have, 0)
    return 0 if gap == 0 else max(4, round(SKILLS[skill_id]["hours"] * gap / 4))


def analyze(profile, completed):
    role = role_or_default(profile.get("target_role"))
    levels = effective_levels(profile, completed)
    rows, earned, possible, hours_left = [], 0.0, 0.0, 0

    for skill_id, (target, weight) in role["skills"].items():
        have = levels.get(skill_id, 0)
        w = WEIGHTS[weight]
        earned += w * min(have, target) / target
        possible += w
        hours = hours_to_close(skill_id, have, target)
        hours_left += hours
        status = "strong" if have >= target else ("missing" if have == 0 else "developing")
        rows.append({
            "id": skill_id, "name": SKILLS[skill_id]["name"], "category": SKILLS[skill_id]["category"],
            "have": have, "target": target, "weight": weight, "status": status,
            "gap": max(target - have, 0), "hours": hours,
            "priority": w * max(target - have, 0),
        })

    rows.sort(key=lambda r: (-r["priority"], -WEIGHTS[r["weight"]], r["name"]))
    readiness = round(100 * earned / possible) if possible else 0
    hpw = max(int(profile.get("hours_per_week") or 8), 1)
    extra = [s for s in levels if s not in role["skills"] and levels[s] > 0]

    return {
        "role_id": profile.get("target_role") if profile.get("target_role") in ROLES else "fullstack",
        "role": role["title"], "icon": role["icon"], "summary": role["summary"],
        "readiness": readiness, "verdict": verdict(readiness),
        "skills": rows,
        "strengths": [r["name"] for r in rows if r["status"] == "strong"],
        "gaps": [r for r in rows if r["gap"] > 0],
        "transferable": [SKILLS[s]["name"] for s in extra],
        "hours_left": hours_left,
        "weeks_left": math.ceil(hours_left / hpw) if hours_left else 0,
        "hours_per_week": hpw,
    }


def verdict(score):
    if score >= 85:
        return "Job-ready — start applying and polishing interviews."
    if score >= 65:
        return "Almost there — close a few key gaps and you're competitive."
    if score >= 40:
        return "Solid foundation — focus on the core skills below."
    return "Early stage — follow the roadmap step by step, you've got this."


# ---------------------------------------------------------------------------
# Personalized learning roadmap
# ---------------------------------------------------------------------------
def build_roadmap(profile, completed):
    report = analyze(profile, completed)
    hpw = report["hours_per_week"]
    phase_of = {"core": "Foundation", "important": "Build", "bonus": "Polish"}
    phases = {"Foundation": [], "Build": [], "Polish": [], "Career Launch": []}

    # Use the self-rated level (not effective) so completed tasks stay visible.
    raw = {k: int(v) for k, v in (profile.get("skills") or {}).items()}
    role = role_or_default(profile.get("target_role"))
    ordered = sorted(role["skills"].items(),
                     key=lambda kv: (-WEIGHTS[kv[1][1]] * max(kv[1][0] - raw.get(kv[0], 0), 0), kv[0]))

    cum = 0  # cumulative hours, used to place each task in a week
    for skill_id, (target, weight) in ordered:
        have = raw.get(skill_id, 0)
        total = hours_to_close(skill_id, have, target)
        if total == 0:
            continue
        skill = SKILLS[skill_id]
        parts = [
            (f"{skill_id}:learn", f"Learn {skill['name']} — {LEVEL_NAMES[have]} → {LEVEL_NAMES[target]}",
             "learn", round(total * 0.5)),
            (f"{skill_id}:practice", f"Practice {skill['name']} with daily exercises", "practice",
             round(total * 0.2)),
            (f"{skill_id}:project", f"Project: {skill['project']}", "project", round(total * 0.3)),
        ]
        tasks = []
        for task_id, title, kind, hours in parts:
            hours = max(hours, 1)
            tasks.append({"id": task_id, "title": title, "kind": kind, "hours": hours,
                          "week": cum // hpw + 1, "done": task_id in completed})
            cum += hours
        phases[phase_of[weight]].append({
            "skill_id": skill_id, "skill": skill["name"], "weight": weight,
            "have": have, "target": target, "hours": total,
            "resources": [{"title": t, "url": u} for t, u in skill["resources"]],
            "tasks": tasks,
            "done": all(t["done"] for t in tasks),
        })

    week = cum // hpw + 1
    phases["Career Launch"].append({
        "skill_id": "career", "skill": "Get hired", "weight": "core", "have": 0, "target": 0,
        "hours": sum(h for _, _, h in CAREER_TASKS), "resources": [],
        "tasks": [{"id": i, "title": t, "kind": "career", "hours": h, "week": week, "done": i in completed}
                  for i, t, h in CAREER_TASKS],
        "done": all(i in completed for i, _, _ in CAREER_TASKS),
    })

    all_tasks = [t for p in phases.values() for item in p for t in item["tasks"]]
    done = sum(1 for t in all_tasks if t["done"])
    return {
        "role": report["role"], "hours_per_week": hpw,
        "total_weeks": math.ceil((cum + sum(h for _, _, h in CAREER_TASKS)) / hpw),
        "total_tasks": len(all_tasks), "done_tasks": done,
        "percent": round(100 * done / len(all_tasks)) if all_tasks else 0,
        "phases": [{"name": n, "items": items} for n, items in phases.items() if items],
        "next_task": next((t for t in all_tasks if not t["done"]), None),
    }


def valid_task_ids(profile):
    role = role_or_default(profile.get("target_role"))
    ids = {i for i, _, _ in CAREER_TASKS}
    for skill_id in role["skills"]:
        ids.update(task_ids_for_skill(skill_id))
    return ids


# ---------------------------------------------------------------------------
# Resume analyzer
# ---------------------------------------------------------------------------
ACTION_VERBS = ["built", "developed", "designed", "led", "created", "implemented", "improved",
                "launched", "optimized", "reduced", "increased", "managed", "automated", "deployed",
                "analyzed", "delivered", "collaborated", "mentored", "architected", "researched"]
SECTIONS = {
    "Contact info": [r"[^@\s]+@[^@\s]+\.[a-z]{2,}", r"\+?\d[\d\s-]{8,}\d", r"linkedin", r"github\.com"],
    "Education": [r"\beducation\b", r"\bb\.?tech\b", r"\bbachelor", r"\bdegree\b", r"\buniversity\b", r"\bcollege\b"],
    "Experience": [r"\bexperience\b", r"\bintern(ship)?\b", r"\bemployment\b", r"\bwork history\b"],
    "Projects": [r"\bprojects?\b"],
    "Skills": [r"\bskills\b", r"\btechnologies\b", r"\btech stack\b"],
    "Certifications / Achievements": [r"\bcertif", r"\bachievement", r"\baward", r"\bhackathon"],
}


def alias_pattern(alias):
    return re.compile(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])")


ALIAS_PATTERNS = {sid: [alias_pattern(a) for a in s["aliases"]] for sid, s in SKILLS.items()}


def extract_skills(text):
    lower = text.lower()
    found = {}
    for skill_id, patterns in ALIAS_PATTERNS.items():
        hits = sum(len(p.findall(lower)) for p in patterns)
        if hits:
            found[skill_id] = hits
    return found


def estimate_level(hits, text_lower, skill_id):
    """Rough level guess from how a skill is mentioned. Capped at Intermediate:
    a resume shows exposure, not mastery, so the roadmap still covers depth."""
    near_project = any(re.search(r"(built|developed|project|deployed)[^.\n]{0,80}" + re.escape(a), text_lower)
                       for a in SKILLS[skill_id]["aliases"])
    return 3 if hits > 1 or near_project else 2


def analyze_resume(text, role_id):
    text = (text or "").strip()
    lower = text.lower()
    words = re.findall(r"[A-Za-z0-9+#.]+", text)
    found = extract_skills(text)
    role = role_or_default(role_id)

    sections = {name: any(re.search(p, lower) for p in pats) for name, pats in SECTIONS.items()}
    verbs = sorted({v for v in ACTION_VERBS if re.search(r"\b" + v + r"\b", lower)})
    metrics = re.findall(r"\b\d+(?:\.\d+)?\s?(?:%|x\b|\+|k\b|users|students|ms|hours|percent)", lower)

    role_skills = list(role["skills"].keys())
    matched = [s for s in role_skills if s in found]
    missing = [s for s in role_skills if s not in found]
    core = [s for s, (_, w) in role["skills"].items() if w == "core"]
    keyword_score = (sum(WEIGHTS[role["skills"][s][1]] for s in matched)
                     / sum(WEIGHTS[w] for _, w in role["skills"].values()))

    n = len(words)
    length_score = 1.0 if 250 <= n <= 900 else (n / 250 if n < 250 else max(0.5, 900 / n))
    breakdown = {
        "Role keywords": round(35 * keyword_score),
        "Sections": round(20 * sum(sections.values()) / len(sections)),
        "Impact & metrics": round(15 * min(len(metrics) / 4, 1)),
        "Action verbs": round(15 * min(len(verbs) / 6, 1)),
        "Length": round(15 * length_score),
    }
    score = sum(breakdown.values())

    tips = []
    for s in [s for s in missing if s in core][:4]:
        tips.append(f"Add {SKILLS[s]['name']} — it's a core skill for {role['title']}. "
                    f"If you don't have it yet, it's in your roadmap.")
    for name, ok in sections.items():
        if not ok:
            tips.append(f"Add a clear \"{name}\" section.")
    if len(metrics) < 3:
        tips.append("Quantify results: e.g. \"cut load time by 40%\" or \"used by 200 students\".")
    if len(verbs) < 5:
        tips.append("Start bullet points with strong action verbs like Built, Led, Optimized, Deployed.")
    if n < 250:
        tips.append(f"Your resume is short ({n} words). Aim for 300–700 words with project details.")
    elif n > 900:
        tips.append(f"Your resume is long ({n} words). Trim to one page for early-career roles.")
    if not tips:
        tips.append("Strong resume! Tailor the summary line to each job you apply for.")

    return {
        "score": score, "breakdown": breakdown, "word_count": n,
        "role": role["title"],
        "skills_found": [{"id": s, "name": SKILLS[s]["name"], "mentions": h,
                          "suggested_level": estimate_level(h, lower, s)}
                         for s, h in sorted(found.items(), key=lambda kv: -kv[1])],
        "matched": [SKILLS[s]["name"] for s in matched],
        "missing": [{"id": s, "name": SKILLS[s]["name"], "weight": role["skills"][s][1]} for s in missing],
        "sections": sections, "action_verbs": verbs, "metrics_found": len(metrics),
        "tips": tips,
    }


# ---------------------------------------------------------------------------
# Interview coach
# ---------------------------------------------------------------------------
def get_question(qid):
    skill_id, _, idx = qid.partition(":")
    bank = BEHAVIORAL_QUESTIONS if skill_id == "behavioral" else QUESTIONS.get(skill_id)
    if not bank or not idx.isdigit() or int(idx) >= len(bank):
        return None
    q, points, tip = bank[int(idx)]
    label = "Behavioral" if skill_id == "behavioral" else SKILLS[skill_id]["name"]
    return {"id": qid, "skill": label, "question": q, "points": points, "tip": tip}


def interview_set(profile, completed, focus=None):
    """Questions for the target role, weakest skills first, plus behavioral."""
    report = analyze(profile, completed)
    skill_order = [r["id"] for r in report["skills"]]
    if focus in QUESTIONS:
        skill_order = [focus]
    out = []
    for skill_id in skill_order:
        for i in range(len(QUESTIONS.get(skill_id, []))):
            q = get_question(f"{skill_id}:{i}")
            out.append({k: q[k] for k in ("id", "skill", "question", "tip")})
    if focus in (None, "", "behavioral"):
        for i in range(len(BEHAVIORAL_QUESTIONS)):
            q = get_question(f"behavioral:{i}")
            out.append({k: q[k] for k in ("id", "skill", "question", "tip")})
    return out


def point_found(point, answer):
    if point in answer:
        return True
    words = [w for w in re.findall(r"[a-z0-9()/+-]+", point) if len(w) > 2]
    return bool(words) and all(w[:5] in answer for w in words)


def evaluate_answer(qid, answer):
    q = get_question(qid)
    if not q:
        return None
    text = (answer or "").lower()
    n_words = len(text.split())
    hit = [p for p in q["points"] if point_found(p, text)]
    miss = [p for p in q["points"] if p not in hit]
    coverage = len(hit) / len(q["points"])
    has_example = bool(re.search(r"for example|for instance|e\.g\.|such as|in my project|i built|i used|\d", text))

    score = round(65 * min(coverage / 0.7, 1) + 20 * min(n_words / 60, 1) + 15 * has_example)
    if n_words < 8:
        score = min(score, 20)

    feedback = []
    if coverage >= 0.7:
        feedback.append("Great coverage of the key concepts.")
    elif coverage >= 0.4:
        feedback.append("Good start — a few important concepts are missing.")
    else:
        feedback.append("Your answer misses most key concepts. Review the tip and try again.")
    if n_words < 40:
        feedback.append("Expand your answer: aim for 60–150 words in an interview.")
    if not has_example:
        feedback.append("Add a concrete example from a project — interviewers love specifics.")

    return {"score": score, "covered": hit, "missing": miss, "feedback": feedback,
            "tip": q["tip"], "grade": "Excellent" if score >= 80 else "Good" if score >= 60
            else "Fair" if score >= 40 else "Needs work"}


# ---------------------------------------------------------------------------
# Job matching
# ---------------------------------------------------------------------------
def match_jobs(profile, completed):
    levels = effective_levels(profile, completed)
    target = profile.get("target_role")
    results = []
    for job in JOBS:
        parts = [min(levels.get(s, 0), JOB_READY_LEVEL) / JOB_READY_LEVEL for s in job["skills"]]
        score = round(100 * sum(parts) / len(parts))
        if job["role"] == target:
            score = min(100, score + 5)
        results.append({
            **{k: job[k] for k in ("id", "title", "company", "location", "type")},
            "role": ROLES[job["role"]]["title"],
            "match": score,
            "have": [SKILLS[s]["name"] for s in job["skills"] if levels.get(s, 0) >= JOB_READY_LEVEL],
            "need": [SKILLS[s]["name"] for s in job["skills"] if levels.get(s, 0) < JOB_READY_LEVEL],
        })
    results.sort(key=lambda j: -j["match"])
    return results


# ---------------------------------------------------------------------------
# AI Mentor chat (intent-based)
# ---------------------------------------------------------------------------
def find_skill_in(text):
    for skill_id, patterns in ALIAS_PATTERNS.items():
        if any(p.search(text) for p in patterns) or SKILLS[skill_id]["name"].lower() in text:
            return skill_id
    return None


def find_role_in(text):
    for role_id, role in ROLES.items():
        if role["title"].lower().split(" /")[0] in text or role_id.replace("_", " ") in text:
            return role_id
    return None


def mentor_reply(message, profile, completed, name="there"):
    text = (message or "").lower().strip()
    report = analyze(profile, completed)
    roadmap = build_roadmap(profile, completed)
    gaps = report["gaps"]
    first = name.split()[0] if name else "there"

    def has(*words):
        return any(w in text for w in words)

    if not text:
        return "Ask me anything about your career path, skills, resume or interviews!"

    if has("hello", "hi ", "hey") and len(text) < 20 or text in ("hi", "hey"):
        return (f"Hi {first}! 👋 You're aiming for **{report['role']}** and you're "
                f"**{report['readiness']}%** ready. Ask me \"what should I learn next?\" to get going.")

    if has("ready", "score", "progress", "how am i", "how far"):
        strong = ", ".join(report["strengths"][:4]) or "none yet"
        return (f"Your readiness for **{report['role']}** is **{report['readiness']}%**. "
                f"{report['verdict']}\n\nStrong skills: {strong}. "
                f"You've completed {roadmap['done_tasks']} of {roadmap['total_tasks']} roadmap tasks.")

    if has("how long", "time", "weeks", "months"):
        if not report["hours_left"]:
            return "You've already reached every target level — you're ready to apply! 🎉"
        return (f"At {report['hours_per_week']} hours/week you need about **{report['hours_left']} hours**, "
                f"or roughly **{report['weeks_left']} weeks**. Increase your weekly hours in your profile "
                "to speed this up.")

    if has("project", "portfolio", "build"):
        ideas = [f"• **{g['name']}** — {SKILLS[g['id']]['project']}" for g in gaps[:3]]
        if not ideas:
            ideas = ["• Combine your skills into one end-to-end app and deploy it publicly."]
        return "Here are portfolio projects that close your biggest gaps:\n" + "\n".join(ideas)

    if has("resume", "cv"):
        return ("Resume quick wins:\n• Lead each bullet with an action verb (Built, Led, Optimized)\n"
                "• Add numbers: users, % improvement, time saved\n"
                f"• Include core {report['role']} keywords\n• Keep it to one page\n\n"
                "Paste your resume in the **Resume Analyzer** for a full score.")

    if has("interview", "mock"):
        weakest = gaps[0]["id"] if gaps else None
        qs = QUESTIONS.get(weakest) or BEHAVIORAL_QUESTIONS
        q, _, tip = qs[0]
        return (f"Try this one:\n\n**{q}**\n\nTip: {tip}\n\nOpen the **Interview Coach** to answer it "
                "and get a score.")

    if has("job", "apply", "hiring", "internship", "company"):
        top = match_jobs(profile, completed)[:3]
        lines = [f"• {j['title']} at {j['company']} — **{j['match']}% match**" for j in top]
        return "Your best job matches right now:\n" + "\n".join(lines)

    if has("stuck", "motivat", "demotivat", "hard", "give up", "tired", "confused"):
        nt = roadmap["next_task"]
        step = f" Your next small step: **{nt['title']}** (~{nt['hours']}h)." if nt else ""
        return ("Feeling stuck is part of learning — everyone hits it. Break the work into 25-minute "
                "sessions and focus on just one task today." + step)

    role_id = find_role_in(text)
    if role_id and has("switch", "become", "about", "what is", "change", "role", "career"):
        role = ROLES[role_id]
        skills = ", ".join(SKILLS[s]["name"] for s in role["skills"])
        return (f"{role['icon']} **{role['title']}** — {role['summary']}\n\nKey skills: {skills}.\n\n"
                "Change your target role in **My Profile** to get a new analysis and roadmap.")

    skill_id = find_skill_in(text)
    if skill_id:
        s = SKILLS[skill_id]
        res = "\n".join(f"• [{t}]({u})" for t, u in s["resources"])
        lvl = LEVEL_NAMES[effective_levels(profile, completed).get(skill_id, 0)]
        return (f"**{s['name']}** (your level: {lvl}). About {s['hours']} hours to get job-ready.\n\n"
                f"Best free resources:\n{res}\n\nProject idea: {s['project']}")

    if has("next", "learn", "start", "what should", "focus", "recommend", "suggest"):
        if not gaps:
            return "You've hit every target! Head to **Job Matches** and start applying. 🚀"
        g = gaps[0]
        nt = roadmap["next_task"]
        return (f"Focus on **{g['name']}** next — it's a {g['weight']} skill for {report['role']} "
                f"and you're at level {g['have']}/{g['target']}.\n\n"
                + (f"Next task: **{nt['title']}** (~{nt['hours']}h)." if nt else ""))

    return ("I can help with:\n• \"What should I learn next?\"\n• \"How ready am I?\"\n"
            "• \"How long will it take?\"\n• \"Suggest a project\"\n• \"Give me an interview question\"\n"
            "• \"Show my job matches\"\n• Any skill, e.g. \"How do I learn Docker?\"")
