# MASTER PROMPT — Deepfake Interview Alert Tool (3-Player Speedrun Build)

Paste this **entire file** into each of the 3 players' OpenCode agents. It is
the same master prompt for all three — the only difference per player is the
`## Your Role` section they act on. All three agents work in the **same repo**,
in parallel, and stay in sync through `AGENT_SYNC.md` (protocol below).

---

## Project

**Deepfake Interview Alert Tool** — TCS Tech Day @ Vidyavardhini College of
Engineering (Theme: AI • Cyber Defense). A prototype that compares a
candidate's claimed skills (resume/profile) against interview answer quality
and manually-logged observation notes, and produces an **impersonation risk
score** to support — never replace — interviewer judgment.

**Stack (fixed):** Python 3.11.9 · NiceGUI (frontend) · plain Python
lists/dicts as the in-memory data store (no DB/ORM) · `scikit-learn`
TF-IDF + cosine similarity for the NLP signal (offline, no API keys, no
network calls) · synthetic data only, zero real biometric/audio/video data.

**Hard rule for every player, every file:** the tool outputs a `score (0-100)`,
a `risk_label (Low/Medium/High)`, and `2-3 reasons`. It **never** outputs a
hire/reject verdict, and every result surface (UI, logs, docs) must carry:
*"This score supports interviewer review and does not make a hiring decision."*

---

## Shared Contract (do not deviate without logging it — see sync protocol)

Whoever's agent runs first creates `models.py` with these dataclasses. Every
other player builds against this exact shape:

```python
@dataclass
class CandidateProfile:
    candidate_id: str
    name: str
    claimed_skills: list[str]
    resume_text: str

@dataclass
class InterviewResponse:
    candidate_id: str
    question: str
    expected_skill: str
    answer_text: str
    observation_flags: list[str]  # e.g. ["prompting_suspected", "low_eye_contact"]
    # NOTE: observation_flags are MANUALLY entered/simulated — never derived
    # from real audio/video/biometric analysis in this prototype.

@dataclass
class RiskAssessment:
    candidate_id: str
    score: int              # 0-100
    risk_label: str         # "Low" | "Medium" | "High"
    reasons: list[str]      # 2-3 short human-readable reasons
    disclaimer: str = "This score supports interviewer review and does not make a hiring decision."
```

---

## Inter-Agent Sync Protocol — `AGENT_SYNC.md`

This is how three separate AI agents, working in parallel with no direct
communication, stay aware of each other's progress. **This is not optional.**

**Before touching any file**, your agent must:
1. Open and read `AGENT_SYNC.md` in full (create it if it doesn't exist yet,
   using the template below).
2. Note which files/interfaces other players have already created — build
   against what exists rather than re-defining it.

**After every meaningful unit of work** (a new function, a finished module, a
bugfix that changes an interface), your agent must **append** (never overwrite
or delete prior entries) a new entry to `AGENT_SYNC.md`:

```markdown
### [HH:MM] Player <A/B/C> — <role name>
**Files touched:** path/to/file.py, path/to/other.py
**What changed:** one or two sentences, plain language
**New interface available for others:** function/class signature + one-line
usage example, if this is something the other two agents will call
**Open questions / blockers:** anything another player needs to resolve, or
"none"
```

**Template to create `AGENT_SYNC.md` with, if it doesn't exist:**

```markdown
# Agent Sync Log
Shared context file. Every agent reads this before working and appends an
entry after each unit of work. Never edit or delete another agent's entry —
only append.

---
```

If your agent is about to build something that conflicts with an existing
logged entry (e.g., changing a dataclass field another player already
depends on), it must **stop and flag it in the sync log as a blocker**
instead of silently changing the shared contract.

---

## Security Constraints (apply regardless of role)

**Backend / logic layer:**
- Never use `eval`, `exec`, `pickle.loads` on any user-supplied text.
- Treat all resume/answer/observation text as untrusted input: validate
  type and enforce a max length (e.g. 5,000 chars) before processing;
  reject/trim silently-truncate rather than crash on oversized input.
- No real PII/biometric fields anywhere in the data model — synthetic data
  only, and reject any field that looks like an email, phone number, or ID
  number pattern in demo data with a lint/check, not just a convention.
- No network calls from the scoring pipeline (TF-IDF is local/offline) —
  if a player later wants a hosted embedding API, that requires explicit
  confirmation from the team, not a silent addition.
- No hardcoded secrets/API keys anywhere in code, fixtures, or docs, even
  placeholder-looking ones.
- Fail closed: if scoring inputs are malformed, return a clearly-labeled
  error/low-confidence result — never a fabricated score.

**Frontend (NiceGUI):**
- Escape/sanitize all user-entered text before rendering it back (resume
  text, answers, notes) — never render untrusted text as raw HTML.
- Enforce input length limits in the UI layer too, not just the backend
  (defense in depth).
- No arbitrary file upload/execution — if resume upload is added, restrict
  to plain text/PDF text-extraction only, no execution of uploaded content.
- The "advisory only, not a hiring decision" disclaimer must be visually
  present on every results view, not just in code comments.
- No client-side storage of candidate data beyond the current session.

---

## Division of Work — 3 Players

### Player A — Data + NLP/ML Engineer
**Owns:** `data/synthetic_candidates.py`, `services/nlp_match.py`

- Build 8–10 synthetic `CandidateProfile` + `InterviewResponse` records
  covering: clean match, clear skill-mismatch (e.g. claims ML, can't explain
  training steps), borderline case, suspicious-observation-flags case.
- Implement `nlp_match.py`: TF-IDF vectorize `claimed_skills` + `resume_text`
  against `answer_text`; return a per-skill cosine similarity score and an
  overall similarity signal (0–1 float), with reasoning strings like
  `"Low similarity between claimed skill 'Machine Learning' and answer content"`.
- Apply the backend input-validation security constraints (length limits,
  no eval/exec, no PII fields) to your own data generation and matching code.
- Log your dataclass usage and function signatures in `AGENT_SYNC.md` as
  soon as `nlp_match.py`'s main function is callable — Player B needs it.

### Player B — Rules + Scoring Aggregation + Backend Security Engineer
**Owns:** `services/rules.py`, `services/scoring.py`, security hardening for the backend

- Implement `rules.py`: canned/generic-phrase detection, answer length vs.
  expected depth per question, observation-flag penalty rules (e.g.
  `"prompting_suspected"` → risk bump), reason-string generation.
- Implement `scoring.py`: combine Player A's similarity signal + your rule
  signals into one weighted `RiskAssessment` (0–100 score, Low/Medium/High
  label via documented thresholds, 2–3 reasons). Pure, idempotent function —
  same input always gives same output.
- Own and enforce the backend security constraints above across the whole
  pipeline (input validation, no network calls, fail-closed behavior).
- Log the final `scoring.py` entrypoint signature in `AGENT_SYNC.md` —
  Player C wires the UI directly to it.

### Player C — Frontend (NiceGUI) + Integration + Frontend Security Engineer
**Owns:** `app/main.py`, NiceGUI pages, wiring to `scoring.py`

- Build the input screen: candidate profile fields, interview answer text
  areas, transcript/observation notes with manual flag toggles.
- Build the results screen: score, risk-label badge, reasons list,
  disclaimer banner — pulling live from Player B's `scoring.py`, not mocked
  data, once it's available (check `AGENT_SYNC.md` for the entrypoint).
- Apply all frontend security constraints (escaping, input limits, no raw
  HTML render of untrusted text, disclaimer always visible).
- Prepare the demo flow: clean-match candidate → low risk; planted mismatch
  candidate → high risk with visible reasons.
- Log every UI/integration milestone in `AGENT_SYNC.md` so Players A and B
  know when their modules have been successfully wired in and can adjust
  interfaces if the UI needs a different shape.

---

## Response Style for all 3 agents

- Small, local changes (styling, a fixture tweak): make the change, brief
  explanation, no ceremony.
- Anything touching the shared `models.py` contract or scoring thresholds:
  explain the reasoning, show before/after example output, and log it in
  `AGENT_SYNC.md` before considering it done.
- Never commit/push/create branches without explicit confirmation from your
  player.
- Never skip the `AGENT_SYNC.md` read-before/append-after step, even for
  small changes — that log is the only thing keeping three parallel agents
  coordinated.
