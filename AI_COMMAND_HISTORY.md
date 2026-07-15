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
