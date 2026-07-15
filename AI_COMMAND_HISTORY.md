# AI Command History

Purpose: an append-only, human- and AI-readable log where agents record the
commands/prompts they used to generate or change code, and the rationale for
those changes. This helps future AI agents understand *why* code exists and
how to adapt it safely.

Format (append-only):

```markdown
### [ISO timestamp] — Agent: <player or tool>
**Action:** create / update / refactor / fix
**Files:** path/to/file(s)
**Command / Prompt Used:** short copy or summary of the prompt/command
**Rationale (why):** brief explanation of why the change was made
**Notes for other agents:** how to adapt, expected inputs/outputs, compatibility
```

---

Initial entries

### 2026-07-15T12:00:00Z — Agent: assistant
**Action:** update prompt
**Files:** deepfake-tool-3player-master-prompt.md
**Command / Prompt Used:** "Update this prompt for a 1 hour hackathon and create a command history file for other AI agents to understand why or other code context they have written with an AI agent."
**Rationale (why):** Timebox the project to 60 minutes, reduce scope to an MVP,
and add `AI_COMMAND_HISTORY.md` as a required append-only artifact so agents
can record the prompts/commands and rationale behind AI-written changes. This
helps later agents debug intent and avoid silent contract-breaking edits.
**Notes for other agents:** Always append entries to this file when you run
an AI-generated code change that other agents will rely on. Do not overwrite.

### 2026-07-15T14:30:00Z — Agent: Player C (UI & Integration)
**Action:** create
**Files:** app/main.py, models.py, services/scoring.py, data/synthetic_candidates.py, requirements.txt
**Command / Prompt Used:** "i am player C make frontend with refrence which has already been given . Also while making it make sure you don't finish my credits. and also make sure i don't have to debug later. also add ui components that you think are important.add all the to do's in file name AI_COMMAND_HISTORY.md"
**Rationale (why):** Implemented a complete frontend dashboard using NiceGUI matching the glassmorphic Crextio visual layout. Added stub files for core contract dataclasses (`models.py`), scoring logic (`services/scoring.py`), and candidate datasets (`data/synthetic_candidates.py`) to prevent import errors and ensure immediate offline execution.
**Notes for other agents:** Other players can drop in their real NLP matching and scoring rule libraries into `services/` and `models.py`. The frontend utilizes standard calls to `calculate_risk(profile, response)`.
