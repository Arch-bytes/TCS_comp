from __future__ import annotations

import sys
from pathlib import Path

from nicegui import ui

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.synthetic_candidates import CANDIDATES
from models import CandidateProfile, InterviewResponse
from services.scoring import MAX_INPUT_LENGTH, score_candidate

PAGE_CSS = """
<style>
:root {
    --bg-a: #08111f;
    --bg-b: #0f1f33;
    --card: rgba(11, 19, 34, 0.84);
    --card-border: rgba(148, 163, 184, 0.18);
    --text: #ecf3ff;
    --muted: #a6b3c7;
}

body {
    margin: 0;
    background: radial-gradient(circle at top left, #173155 0%, transparent 28%),
                radial-gradient(circle at top right, #10284b 0%, transparent 24%),
                linear-gradient(160deg, var(--bg-a), var(--bg-b));
    color: var(--text);
    font-family: "Segoe UI", "Aptos", sans-serif;
    color-scheme: dark;
}

.page-shell { min-height: 100vh; padding: 28px; }
.hero {
    border: 1px solid var(--card-border);
    background: linear-gradient(180deg, rgba(21, 31, 48, 0.92), rgba(11, 19, 34, 0.82));
    box-shadow: 0 24px 60px rgba(3, 7, 18, 0.35);
    border-radius: 24px;
}
.panel {
    border: 1px solid var(--card-border);
    background: var(--card);
    box-shadow: 0 20px 50px rgba(3, 7, 18, 0.24);
    border-radius: 22px;
}
.muted { color: var(--muted); }
.score-ring {
    width: 150px;
    height: 150px;
    border-radius: 9999px;
    display: grid;
    place-items: center;
    border: 10px solid rgba(103, 232, 249, 0.35);
    background: radial-gradient(circle, rgba(18, 37, 62, 0.92), rgba(9, 16, 28, 0.95));
}
.score-good { border-color: rgba(34, 197, 94, 0.75); }
.score-warn { border-color: rgba(245, 158, 11, 0.78); }
.score-bad { border-color: rgba(239, 68, 68, 0.78); }
.pill {
    border-radius: 9999px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.pill-good { background: rgba(34, 197, 94, 0.18); color: #86efac; }
.pill-warn { background: rgba(245, 158, 11, 0.18); color: #fcd34d; }
.pill-bad { background: rgba(239, 68, 68, 0.18); color: #fca5a5; }
.pill-info { background: rgba(103, 232, 249, 0.14); color: #a5f3fc; }
.reason-list > div {
    border-top: 1px solid rgba(148, 163, 184, 0.12);
    padding-top: 10px;
    margin-top: 10px;
}
.tiny { font-size: 12px; color: var(--muted); }

.section-kicker {
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(165, 243, 252, 0.92);
}

.section-title {
    font-size: 22px;
    line-height: 1.15;
    font-weight: 800;
    color: var(--text);
}

.subtle-chip {
    border-radius: 9999px;
    padding: 4px 10px;
    background: rgba(103, 232, 249, 0.1);
    color: #c9fbff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.ml-card {
    border: 1px solid rgba(103, 232, 249, 0.12);
    background: linear-gradient(180deg, rgba(11, 19, 34, 0.95), rgba(8, 14, 25, 0.92));
}

.field-note {
    margin-top: -6px;
    margin-bottom: 8px;
    font-size: 11px;
    color: rgba(165, 180, 252, 0.92);
}

.q-field,
.q-field__native,
.q-field__input,
.q-field__prefix,
.q-field__suffix,
.q-field__label,
.q-field__messages,
.q-field__bottom,
.q-checkbox__label,
.q-item__label,
.q-item__section,
.q-select__dropdown-icon,
.q-icon {
    color: var(--text) !important;
}

.q-field--outlined .q-field__control,
.q-field--filled .q-field__control,
.q-field--standout .q-field__control {
    background: rgba(7, 12, 22, 0.55) !important;
    border-color: rgba(148, 163, 184, 0.22) !important;
}

.q-field--outlined .q-field__control:before,
.q-field--outlined .q-field__control:after {
    border-color: rgba(103, 232, 249, 0.35) !important;
}

.q-field.q-field--focused .q-field__control {
    border-color: rgba(103, 232, 249, 0.75) !important;
}

.q-field textarea,
.q-field input {
    color: var(--text) !important;
    caret-color: var(--accent, #67e8f9) !important;
}

.q-field input::placeholder,
.q-field textarea::placeholder {
    color: rgba(236, 243, 255, 0.48) !important;
    opacity: 1 !important;
}

.q-menu,
.q-dialog__inner .q-card,
.q-list {
    background: rgba(8, 17, 31, 0.98) !important;
    color: var(--text) !important;
}

.q-checkbox__bg {
    color: rgba(236, 243, 255, 0.9) !important;
}
</style>
"""


class AppState:
    def __init__(self) -> None:
        self.sample_index = 0
        self.candidate_name = ""
        self.candidate_id = ""
        self.claimed_skills = ""
        self.resume_text = ""
        self.question = ""
        self.expected_skill = ""
        self.answer_text = ""
        self.observation_flags: set[str] = set()


state = AppState()

candidate_select = None
candidate_name_input = None
candidate_id_input = None
claimed_skills_input = None
resume_input = None
question_input = None
expected_skill_input = None
answer_input = None
flag_checkboxes: dict[str, object] = {}
resume_counter = None
answer_counter = None
score_value = None
risk_pill = None
result_detail = None
reason_panel = None
result_ring = None


def _clip(text: str | None) -> str:
    return (text or "")[:MAX_INPUT_LENGTH]


def _load_sample(index: int) -> None:
    sample = CANDIDATES[index]
    profile = sample["profile"]
    response = sample["response"]
    state.sample_index = index
    state.candidate_name = profile.name
    state.candidate_id = profile.candidate_id
    state.claimed_skills = ", ".join(profile.claimed_skills)
    state.resume_text = profile.resume_text
    state.question = response.question
    state.expected_skill = response.expected_skill
    state.answer_text = response.answer_text
    state.observation_flags = set(response.observation_flags)


def _sync_form() -> None:
    candidate_select.value = str(state.sample_index)
    candidate_name_input.value = state.candidate_name
    candidate_id_input.value = state.candidate_id
    claimed_skills_input.value = state.claimed_skills
    resume_input.value = state.resume_text
    question_input.value = state.question
    expected_skill_input.value = state.expected_skill
    answer_input.value = state.answer_text
    for flag_name, checkbox in flag_checkboxes.items():
        checkbox.value = flag_name in state.observation_flags
    _refresh_counters()


def _refresh_counters() -> None:
    resume_counter.text = f"{len(state.resume_text or '')} / {MAX_INPUT_LENGTH} chars"
    answer_counter.text = f"{len(state.answer_text or '')} / {MAX_INPUT_LENGTH} chars"


def _set_badge(label: str) -> None:
    risk_pill.classes(remove="pill-good pill-warn pill-bad")
    result_styles = {"Low": "pill-good", "Medium": "pill-warn", "High": "pill-bad"}
    risk_pill.classes(add=result_styles.get(label, "pill-info"))


def _render_result(assessment) -> None:
    score_value.text = str(assessment.score)
    risk_pill.text = f"{assessment.risk_label} risk"
    _set_badge(assessment.risk_label)

    ring_styles = {"Low": "score-good", "Medium": "score-warn", "High": "score-bad"}
    result_ring.classes(remove="score-good score-warn score-bad")
    result_ring.classes(add=ring_styles.get(assessment.risk_label, "score-good"))

    if assessment.reasons and assessment.reasons[0].startswith("Low-confidence error"):
        result_detail.text = "Low-confidence result returned because the input failed validation."
    else:
        result_detail.text = "Review the reasons below. Higher scores indicate a higher impersonation risk signal."

    reason_panel.clear()
    with reason_panel:
        for reason in assessment.reasons:
            tone = "text-red-200"
            icon_name = "error"
            lower_reason = reason.lower()
            if "error" in lower_reason or "failed closed" in lower_reason:
                icon_name = "report"
            elif "warning" in lower_reason or "short" in lower_reason or "low" in lower_reason:
                tone = "text-amber-200"
                icon_name = "warning"
            elif (
                "consistent" in lower_reason
                or "no suspicious" in lower_reason
                or "strong" in lower_reason
                or "top claimed skill match" in lower_reason
            ):
                tone = "text-emerald-200"
                icon_name = "check_circle"
            elif "runner-up skill match" in lower_reason:
                tone = "text-cyan-200"
                icon_name = "insights"
            with ui.row().classes("items-start gap-2 reason-row"):
                ui.icon(icon_name, size="sm", color="white")
                ui.label(reason).classes(f"text-sm {tone}")


def evaluate() -> None:
    profile = CandidateProfile(
        candidate_id=_clip(candidate_id_input.value).strip() or "UNKNOWN",
        name=_clip(candidate_name_input.value).strip() or "Unknown Candidate",
        claimed_skills=[skill.strip() for skill in _clip(claimed_skills_input.value).split(",") if skill.strip()],
        resume_text=_clip(resume_input.value),
    )
    response = InterviewResponse(
        candidate_id=profile.candidate_id,
        question=_clip(question_input.value),
        expected_skill=_clip(expected_skill_input.value),
        answer_text=_clip(answer_input.value),
        observation_flags=sorted(flag for flag in state.observation_flags if flag),
    )
    assessment = score_candidate(profile, response)
    _render_result(assessment)


def on_sample_change(event) -> None:
    selected_index = int(event.value)
    _load_sample(selected_index)
    _sync_form()
    evaluate()


def on_flag_change(flag_name: str, checked: bool) -> None:
    if checked:
        state.observation_flags.add(flag_name)
    else:
        state.observation_flags.discard(flag_name)


ui.add_head_html(PAGE_CSS)

with ui.column().classes("page-shell w-full gap-6"):
    with ui.row().classes("hero w-full items-center justify-between px-6 py-5 gap-4"):
        with ui.column().classes("gap-1"):
            ui.label("Deepfake Interview Alert Tool").classes("text-3xl font-bold text-white")
            ui.label(
                "Offline TF-IDF scoring on synthetic interview data. Advisory-only output for interviewer review."
            ).classes("muted text-sm")
        with ui.column().classes("items-end gap-2"):
            ui.label("1-hour hackathon build").classes("pill pill-info")
            ui.label("No network calls, no persistence, no real biometric data.").classes("tiny")

    with ui.row().classes("w-full gap-6 items-start"):
        with ui.card().classes("panel ml-card w-full lg:w-[58%] p-5 gap-4"):
            ui.label("Model Inputs").classes("section-kicker")
            ui.label("Feature set for the interview risk model").classes("section-title")
            ui.label("Load a synthetic case or enter your own transcript and manually logged review notes.").classes("tiny")

            with ui.row().classes("w-full items-center justify-between gap-3"):
                ui.label("Demo flow").classes("subtle-chip")
                ui.label("All fields are synthetic-only and capped at 3000 characters.").classes("tiny")

            candidate_select = ui.select(
                {str(index): f"{sample['profile'].candidate_id} - {sample['profile'].name}" for index, sample in enumerate(CANDIDATES)},
                value="0",
                label="Synthetic case",
                on_change=on_sample_change,
            ).props("outlined")

            with ui.row().classes("w-full gap-3"):
                candidate_id_input = ui.input(label="Synthetic ID", value="", placeholder="CAN-001").props(
                    f"outlined maxlength={MAX_INPUT_LENGTH}"
                ).classes("w-full")
                candidate_name_input = ui.input(label="Persona label", value="", placeholder="Synthetic candidate").props(
                    f"outlined maxlength={MAX_INPUT_LENGTH}"
                ).classes("w-full")

            claimed_skills_input = ui.input(
                label="Claimed capability set",
                value="",
                placeholder="Python, FastAPI, PostgreSQL",
            ).props(f"outlined maxlength={MAX_INPUT_LENGTH}").classes("w-full")
            ui.label("Comma-separated capabilities used as model features.").classes("field-note")

            resume_input = ui.textarea(
                label="Profile / resume text",
                value="",
                placeholder="Paste the candidate's profile summary here.",
            ).props(f"outlined autogrow maxlength={MAX_INPUT_LENGTH}").classes("w-full")
            resume_counter = ui.label("").classes("tiny self-end")

            question_input = ui.input(
                label="Prompt context",
                value="",
                placeholder="How did you use Python in your last backend project?",
            ).props(f"outlined maxlength={MAX_INPUT_LENGTH}").classes("w-full")
            ui.label("Optional context used only for the reviewer workflow.").classes("field-note")

            expected_skill_input = ui.input(
                label="Expected competency",
                value="",
                placeholder="Python",
            ).props(f"outlined maxlength={MAX_INPUT_LENGTH}").classes("w-full")

            answer_input = ui.textarea(
                label="Transcript / answer text",
                value="",
                placeholder="Paste the interview transcript or response here.",
            ).props(f"outlined autogrow maxlength={MAX_INPUT_LENGTH}").classes("w-full")
            answer_counter = ui.label("").classes("tiny self-end")

            with ui.column().classes("w-full gap-2"):
                ui.label("Manual observation notes").classes("text-sm font-semibold text-white")
                ui.label(
                    "These are manually logged reviewer notes only; they are not live video or biometric detection."
                ).classes("tiny")
                flag_specs = [
                    ("lip_sync_error", "Lip-sync mismatch"),
                    ("audio_unsynced", "Audio/video sync issue"),
                    ("multiple_voices", "Multiple voices"),
                    ("unnatural_blink", "Unusual blink pattern"),
                    ("background_swapped", "Background mismatch"),
                    ("head_movement_unnatural", "Unnatural head movement"),
                    ("poor_eye_contact", "Poor eye contact"),
                    ("reading_from_script", "Reading from script"),
                    ("prompting_detected", "Prompting detected"),
                    ("external_assistance", "External assistance"),
                ]
                for flag_name, label in flag_specs:
                    flag_checkboxes[flag_name] = ui.checkbox(
                        label,
                        value=False,
                        on_change=lambda event, name=flag_name: on_flag_change(name, bool(event.value)),
                    ).classes("text-white")

            ui.button("Score candidate", on_click=evaluate).props("unelevated").classes(
                "w-full bg-cyan-400 text-slate-950 font-bold"
            )

        with ui.column().classes("w-full lg:w-[42%] gap-6"):
            with ui.card().classes("panel ml-card p-5 gap-4 items-center text-center"):
                ui.label("Inference Output").classes("section-kicker self-start")
                ui.label("Risk score and explanation").classes("section-title self-start")
                result_ring = ui.column().classes("score-ring score-good")
                with result_ring:
                    score_value = ui.label("0").classes("text-5xl font-bold text-white")
                    ui.label("RISK SCORE").classes("tiny tracking-[0.35em]")

                risk_pill = ui.label("Low risk").classes("pill pill-good")
                result_detail = ui.label("").classes("tiny")

                with ui.row().classes("w-full gap-2 justify-center"):
                    ui.badge("Offline", color="cyan-3")
                    ui.badge("Synthetic data only", color="blue-3")
                    ui.badge("Advisory only", color="green-3")

            with ui.card().classes("panel ml-card p-5 gap-3"):
                ui.label("Why this score?").classes("section-kicker")
                ui.label("Model evidence").classes("section-title")
                ui.label("Reasons are explicit so a judge can see the signal, not a black box.").classes("tiny")
                reason_panel = ui.column().classes("reason-list w-full")

            with ui.card().classes("panel ml-card p-5"):
                ui.label("Safety note").classes("section-kicker")
                ui.label(
                    "This score supports interviewer review and does not make a hiring decision."
                ).classes("text-sm text-cyan-100")
                ui.label(
                    "Scale-up path: keep the scoring contract, then swap in a database, stronger embeddings, and access control later."
                ).classes("tiny mt-2")

_load_sample(0)
_sync_form()
evaluate()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Deepfake Interview Alert Tool", port=8080, reload=True, show=False)
