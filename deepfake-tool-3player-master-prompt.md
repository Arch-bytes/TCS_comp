# MASTER PROMPT — Deepfake Interview Alert Tool (1‑Hour Hackathon, 3 Players)

Paste this entire file into each player's agent. All agents use the same
master prompt; only `## Your Role` differs per player. Timebox: 60 minutes.

Goal: ship a minimal, runnable demo that accepts synthetic candidate data,
computes a `RiskAssessment` (score 0–100, label Low/Medium/High, 2–3 reasons),
and shows results in the UI with a clear disclaimer. Prioritize correctness,
security, and a stable, documented interface other agents can wire to.

High-level constraints
- Timeboxed: implement only the MVP features listed below.
- Synthetic data only. No real audio/biometric/video/PII.
- No network/API calls from the scoring pipeline. All ML is local TF‑IDF.
- Security-first: validate/trim inputs, no `eval`/`exec`/`pickle.loads`.

MVP (60 minute) priorities — in order
1. `models.py` dataclasses and a single small synthetic dataset (6–8 entries).
2. `services/nlp_match.py` — TF‑IDF similarity signal (claimed skills/resume vs answer).
3. `services/rules.py` — 2–3 simple rules (length depth, canned phrase detection,
   observation flag penalty).
4. `services/scoring.py` — deterministic aggregator producing `RiskAssessment`.
5. `app/main.py` — minimal NiceGUI UI that takes inputs, calls `scoring.py`, and
   displays `score`, `risk_label`, `reasons`, and the disclaimer.

If time remains: add 1–2 demo flows and small UI polish (badges, reason bullets).

Shared contract (must be followed)
- `models.py` must define these dataclasses. Do not change fields without
  appending a blocker entry to `AGENT_SYNC.md` and getting agreement.

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
    observation_flags: list[str]

@dataclass
class RiskAssessment:
    candidate_id: str
    score: int
    risk_label: str
    reasons: list[str]
    disclaimer: str = "This score supports interviewer review and does not make a hiring decision."
```

Sync and history files (required)
- `AGENT_SYNC.md`: continue using the existing append-only sync log protocol.
- `AI_COMMAND_HISTORY.md` (new): a short, append-only file where agents record
  the *commands, prompts, and rationale* that produced or changed code. Use
  `AI_COMMAND_HISTORY.md` to help future AI agents understand *why* code was
  added/changed by an agent.

Before changing any shared interface (dataclass fields, function signatures):
1. Read `AGENT_SYNC.md` and `AI_COMMAND_HISTORY.md`.
2. If your change affects others, add a blocker entry in `AGENT_SYNC.md` and
   a rationale entry in `AI_COMMAND_HISTORY.md` explaining why the change is
   necessary and how to adapt.

`AGENT_SYNC.md` append template (same as before):

```markdown
### [HH:MM] Player <A/B/C> — <role>
**Files touched:** path/to/file.py
**What changed:** short plain-language description
**New interface:** function/class signature + example (if relevant)
**Open questions / blockers:** none / explanation
```

`AI_COMMAND_HISTORY.md` append template (new):

```markdown
### [ISO timestamp] — Agent: <player or tool>
**Action:** create/update / refactor / fix
**Files:** path/to/file(s)
**Command / Prompt Used:** short copy of the command or prompt the agent ran
**Rationale (why):** short explanation of why the change was made
**Notes for other agents:** how to adapt, expected inputs/outputs, backward-compat notes
```

Security and demo rules (quick)
- Enforce max-length on text fields (e.g., 5000 chars) and sanitize before UI render.
- Fail closed: return a labeled low-confidence result if inputs are invalid.
- No secrets, no network calls, synthetic-only.

Roles (60-minute scope)
Player A — Data & NLP (tiny scope)
- Create `models.py` and `data/synthetic_candidates.py` with 6 sample pairs.
- Implement `services/nlp_match.py` with TF‑IDF and a simple call `match(candidate, response)`.
Player B — Rules & Scoring (tiny scope)
- Implement `services/rules.py` with 2 rules and `services/scoring.py` that
  consumes `nlp_match` output and returns `RiskAssessment`.
Player C — UI & Integration (tiny scope)
- Implement `app/main.py` NiceGUI form that calls `scoring.py` and displays results.

Quick run (dev machine, Python 3.11+)
1. Create a virtualenv and install requirements: `pip install -r requirements.txt`
2. From project root: `python -m app.main`
3. Open the NiceGUI URL printed by the server and run the demo flows.

Response style
- Make focused changes, append to both `AGENT_SYNC.md` and `AI_COMMAND_HISTORY.md`.
- If you change a contract, show before/after examples and explain impact.

Good luck — keep it small, secure, and demonstrable within 60 minutes.
