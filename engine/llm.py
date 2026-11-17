"""
============================================================================
SkillBridge AI - Claude integration
============================================================================
Uses the official Anthropic SDK (`pip install -r requirements.txt`) to power
the AI Mentor chat and interview answer grading with Claude.

Claude is used only when the SDK is installed AND credentials are present
(ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN). Otherwise - or if a request
fails - every function returns None and the caller falls back to the
offline rule-based engine in ai.py, so the site always works.
============================================================================
"""

import json
import logging
import os

try:
    import anthropic
except ImportError:  # SDK not installed -> offline mode
    anthropic = None

MODEL = os.environ.get("SKILLBRIDGE_MODEL", "claude-opus-5-5")
# Server-side refusal fallback: if Claude declines, the API retries on
# Anthropic's recommended fallback model inside the same call.
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_HISTORY = 12  # mentor messages kept for context

log = logging.getLogger("skillbridge.llm")
_client = None


def enabled():
    has_credentials = bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
    return anthropic is not None and has_credentials


def status():
    if anthropic is None:
        return {"enabled": False, "model": None, "reason": "Anthropic SDK not installed"}
    if not enabled():
        return {"enabled": False, "model": None, "reason": "No ANTHROPIC_API_KEY set"}
    return {"enabled": True, "model": MODEL, "reason": None}


def client():
    global _client
    if _client is None:
        # Short timeout: a web request is waiting on this. One retry on 429/5xx.
        _client = anthropic.Anthropic(timeout=45.0, max_retries=1)
    return _client


def _call(**params):
    """Run one Messages request; return the response text or None on any failure."""
    if not enabled():
        return None
    try:
        response = client().beta.messages.create(
            model=MODEL,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            **params,
        )
    except anthropic.AuthenticationError:
        log.error("Claude: invalid API key - using offline engine")
    except anthropic.RateLimitError:
        log.warning("Claude: rate limited - using offline engine")
    except anthropic.APIStatusError as e:
        log.error("Claude: API error %s: %s", e.status_code, e.message)
    except anthropic.APIConnectionError:
        log.warning("Claude: network error - using offline engine")
    else:
        if response.stop_reason == "refusal":
            log.warning("Claude declined the request (%s)", getattr(response.stop_details, "category", None))
            return None
        text = "".join(b.text for b in response.content if b.type == "text").strip()
        return text or None
    return None


# ---------------------------------------------------------------------------
# AI Mentor
# ---------------------------------------------------------------------------
MENTOR_SYSTEM = """You are the SkillBridge AI Mentor, a warm, practical career coach for students,
fresh graduates and career switchers. You help one learner reach their target role.

How to answer:
- Ground every answer in the learner profile below: their target role, skill levels,
  gaps, roadmap and job matches. Refer to specific skills and numbers from it.
- Be concise: usually 3-8 short sentences or a short bulleted list. Plain, encouraging,
  no fluff.
- When recommending what to learn, prefer the learner's highest-priority gaps (core
  skills first) and their next roadmap task.
- Only recommend resources from the profile's resource list or well-known official docs.
  Never invent job openings, companies, salaries or statistics.
- Point to SkillBridge features when useful: My Profile & Skills, Skill Gap Analysis,
  Learning Roadmap, Resume Analyzer, Interview Coach, Job Matches.
- Formatting: the chat renders only **bold**, [text](https://link) and line breaks.
  Use "• " for bullets. No headings, tables or code blocks.
- Stay on careers, learning and job hunting; politely steer other topics back."""


def learner_context(name, report, roadmap, jobs, resources):
    """Compact text snapshot of the learner, built from the rule-based engine."""
    skills = "\n".join(
        f"- {s['name']}: level {s['have']}/{s['target']} ({s['weight']}, {s['status']}, ~{s['hours']}h to close)"
        for s in report["skills"])
    nt = roadmap.get("next_task")
    job_lines = "\n".join(f"- {j['title']} at {j['company']}: {j['match']}% match; needs {', '.join(j['need']) or 'nothing'}"
                          for j in jobs[:4])
    res_lines = "\n".join(f"- {skill}: " + "; ".join(f"{t} ({u})" for t, u in items)
                          for skill, items in resources.items())
    return f"""<learner_profile>
Name: {name}
Target role: {report['role']} - {report['summary']}
Readiness: {report['readiness']}% ({report['verdict']})
Study time: {report['hours_per_week']} h/week; about {report['hours_left']} h (~{report['weeks_left']} weeks) left
Skills for the role (level 0-5, have/target):
{skills}
Other skills: {', '.join(report['transferable']) or 'none'}
Roadmap: {roadmap['done_tasks']}/{roadmap['total_tasks']} tasks done ({roadmap['percent']}%)
Next roadmap task: {f"{nt['title']} (~{nt['hours']}h, week {nt['week']})" if nt else 'all done'}
Top job matches (sample listings):
{job_lines}
Free resources for the learner's gaps:
{res_lines or '- none'}
</learner_profile>"""


def mentor_reply(message, history, context):
    """history: [{"role": "user"|"assistant", "content": str}, ...] from the chat UI."""
    turns = [t for t in history if t.get("role") in ("user", "assistant") and isinstance(t.get("content"), str)]
    turns = turns[-MAX_HISTORY:]
    while turns and turns[0]["role"] != "user":  # the API needs a user turn first
        turns.pop(0)
    messages = [{"role": t["role"], "content": t["content"][:2000]} for t in turns]
    messages.append({"role": "user", "content": message})
    return _call(
        max_tokens=4000,
        system=MENTOR_SYSTEM + "\n\n" + context,
        output_config={"effort": "low"},  # chat: keep replies quick
        messages=messages,
    )


# ---------------------------------------------------------------------------
# Interview answer grading
# ---------------------------------------------------------------------------
GRADE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "description": "0-100 overall score"},
        "grade": {"type": "string", "enum": ["Excellent", "Good", "Fair", "Needs work"]},
        "covered": {"type": "array", "items": {"type": "string"},
                    "description": "Key points the answer got right (short phrases)"},
        "missing": {"type": "array", "items": {"type": "string"},
                    "description": "Important points missing or wrong (short phrases)"},
        "feedback": {"type": "array", "items": {"type": "string"},
                     "description": "2-4 specific, actionable coaching sentences"},
        "model_answer": {"type": "string",
                         "description": "A strong 80-150 word answer a candidate could give"},
    },
    "required": ["score", "grade", "covered", "missing", "feedback", "model_answer"],
    "additionalProperties": False,
}

GRADER_SYSTEM = """You are a fair, encouraging technical interviewer grading a candidate's spoken-style
answer for an entry-level role. Judge correctness, completeness, clarity and use of a
concrete example (for behavioral questions, the STAR structure).

Scoring guide: 85-100 excellent and hire-ready; 65-84 good with minor gaps; 40-64 fair,
key concepts missing; below 40 mostly incorrect, off-topic or too short.
Grade bands: Excellent >= 80, Good 60-79, Fair 40-59, Needs work < 40.
The reference key points are hints, not a checklist - credit correct ideas in other words,
and penalize factual errors. Write feedback directly to the candidate ("you")."""


def grade_answer(question, role, answer):
    """question: dict from ai.get_question(). Returns a result dict or None."""
    prompt = (f"Role: {role}\nSkill: {question['skill']}\nQuestion: {question['question']}\n"
              f"Reference key points: {', '.join(question['points'])}\n"
              f"Interviewer tip: {question['tip']}\n\n"
              f"<candidate_answer>\n{answer}\n</candidate_answer>")
    text = _call(
        max_tokens=8000,
        system=GRADER_SYSTEM,
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": GRADE_SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    if not text:
        return None
    try:
        result = json.loads(text)
    except ValueError:
        log.error("Claude: grader returned invalid JSON")
        return None
    result["score"] = max(0, min(100, int(result.get("score", 0))))
    return result
