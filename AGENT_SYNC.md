### [14:10] Player B — Rules & Scoring
**Files touched:** services/__init__.py, services/rules.py, services/scoring.py
**What changed:** Added local, deterministic answer rules and the risk-score aggregator. Invalid or oversized input returns a Medium low-confidence review result.
**New interface:** `assess(candidate: CandidateProfile, response: InterviewResponse) -> RiskAssessment` (alias: `score_assessment`). Example: `assessment = assess(candidate, response)`.
**Open questions / blockers:** Player A's `match(candidate, response)` result shape was not present yet. Scoring accepts a float plus common `{similarity: ...}` / `.similarity` wrappers; please return a 0--1 float for the simplest integration.

### [14:19] Player B — Temporary backend demo
**Files touched:** demo_backend_stubs.py
**What changed:** Added an isolated in-memory Player A stub harness to demonstrate low- and high-risk backend outcomes. It does not modify shared contract files.
**New interface:** Run `python demo_backend_stubs.py`; it prints two `RiskAssessment` results.
**Open questions / blockers:** Delete `demo_backend_stubs.py` after Player A's real `models.py` and `services/nlp_match.py` are received.

### [14:25] Player B — Temporary demo cleanup
**Files touched:** demo_backend_stubs.py
**What changed:** Removed the temporary in-memory Player A stub harness after backend verification.
**New interface:** none
**Open questions / blockers:** none
