import sys
import os
from nicegui import ui

# Ensure project root is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import CandidateProfile, InterviewResponse, RiskAssessment
from services.scoring import calculate_risk
from data.synthetic_candidates import CANDIDATES

# Custom Styling (Glassmorphism + Outfit typography + Soft Light Blue Theme)
CUSTOM_HEAD = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

body {
    background: linear-gradient(135deg, #f0f6fc 0%, #e1eefc 100%) !important;
    font-family: 'Outfit', sans-serif !important;
    margin: 0;
    padding: 0;
}

.glass-panel {
    background: rgba(255, 255, 255, 0.75) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.45) !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 30px rgba(148, 163, 184, 0.1) !important;
    transition: all 0.3s ease;
}

.glass-panel:hover {
    box-shadow: 0 14px 40px rgba(148, 163, 184, 0.18) !important;
}

.top-bar {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(10px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.5) !important;
}

.nav-pill {
    font-weight: 500 !important;
    color: #475569 !important;
    border-radius: 9999px !important;
    padding: 6px 16px !important;
}

.nav-pill-active {
    background: #1e3a8a !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 9999px !important;
    padding: 6px 16px !important;
}

.badge-low {
    background: #dcfce7 !important;
    color: #15803d !important;
    border: 1px solid #bbf7d0 !important;
}

.badge-medium {
    background: #fef3c7 !important;
    color: #b45309 !important;
    border: 1px solid #fde68a !important;
}

.badge-high {
    background: #fee2e2 !important;
    color: #b91c1c !important;
    border: 1px solid #fecaca !important;
}

.dial-low {
    border: 6px solid #22c55e !important;
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.2) !important;
}

.dial-medium {
    border: 6px solid #f59e0b !important;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.2) !important;
}

.dial-high {
    border: 6px solid #ef4444 !important;
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.25) !important;
}

.char-counter {
    font-size: 0.75rem !important;
    color: #64748b !important;
}
</style>
"""

# App State definition to hold reactive fields
class AppState:
    def __init__(self):
        # Default with the first candidate in synthetic dataset
        default = CANDIDATES[0]
        self.candidate_name = default["profile"].name
        self.candidate_id = default["profile"].candidate_id
        self.claimed_skills_str = ", ".join(default["profile"].claimed_skills)
        self.resume_text = default["profile"].resume_text
        
        self.question = default["response"].question
        self.expected_skill = default["response"].expected_skill
        self.answer_text = default["response"].answer_text
        self.observation_flags = set(default["response"].observation_flags)
        
        # Risk assessment output fields
        self.risk_score = 0
        self.risk_label = "Low"
        self.risk_reasons = []

    def set_candidate(self, c_index: int):
        cand = CANDIDATES[c_index]
        self.candidate_name = cand["profile"].name
        self.candidate_id = cand["profile"].candidate_id
        self.claimed_skills_str = ", ".join(cand["profile"].claimed_skills)
        self.resume_text = cand["profile"].resume_text
        self.question = cand["response"].question
        self.expected_skill = cand["response"].expected_skill
        self.answer_text = cand["response"].answer_text
        self.observation_flags = set(cand["response"].observation_flags)

# Instantiate global state
state = AppState()

# UI Layout building
ui.add_head_html(CUSTOM_HEAD)

# Header Row (matching reference navigation bar)
with ui.row().classes('w-full items-center justify-between px-6 py-4 top-bar mb-6 shadow-sm'):
    with ui.row().classes('items-center gap-3'):
        ui.avatar('security', color='primary', size='40px', text_color='white')
        ui.label('Crextio').classes('text-2xl font-bold text-slate-800 tracking-tight')
        ui.label('Deepfake Interview Guard').classes('text-sm text-slate-500 font-medium ml-2')
        
    with ui.row().classes('items-center gap-2 hide-on-mobile'):
        ui.button('Dashboard', color='primary').classes('nav-pill-active')
        ui.button('People').classes('nav-pill flat')
        ui.button('Hiring').classes('nav-pill flat')
        ui.button('Devices').classes('nav-pill flat')
        ui.button('Settings').classes('nav-pill flat')

    with ui.row().classes('items-center gap-4'):
        ui.avatar('person', color='slate-200', size='36px', text_color='slate-600')

# Main Grid Layout
with ui.row().classes('w-full px-6 gap-6 justify-center'):
    
    # 1. Left Section: Presets & Profile Details
    with ui.column().classes('w-full lg:w-[32%] gap-6'):
        # Preset Quick-Load Card
        with ui.card().classes('w-full glass-panel p-5'):
            ui.label('Select Demo Flow').classes('text-lg font-bold text-slate-800 mb-2')
            ui.label('Instantly simulate low, medium, and high-risk candidates.').classes('text-xs text-slate-500 mb-4')
            
            # Preset selector buttons with colored labels
            preset_options = {i: f'{c["profile"].name} ({c["description"].split(" (")[1].replace(")", "")})' for i, c in enumerate(CANDIDATES)}
            
            def load_preset(e):
                state.set_candidate(e.value)
                refresh_all_inputs()
                trigger_analysis()
                ui.notify(f"Loaded Profile: {state.candidate_name}", type='info')

            preset_select = ui.select(
                options=preset_options,
                value=0,
                on_change=load_preset
            ).classes('w-full').props('outlined dense')

        # Candidate Profile Form
        with ui.card().classes('w-full glass-panel p-5'):
            with ui.row().classes('items-center justify-between w-full mb-3'):
                ui.label('Candidate Profile').classes('text-lg font-bold text-slate-800')
                ui.label(state.candidate_id).bind_text_from(state, 'candidate_id').classes('text-xs font-mono text-slate-400')
            
            candidate_name_input = ui.input(
                label='Candidate Name',
                value=state.candidate_name,
                on_change=lambda e: setattr(state, 'candidate_name', e.value)
            ).classes('w-full').props('outlined dense')
            
            claimed_skills_input = ui.input(
                label='Claimed Skills (comma separated)',
                value=state.claimed_skills_str,
                on_change=lambda e: setattr(state, 'claimed_skills_str', e.value)
            ).classes('w-full mt-2').props('outlined dense')
            
            # Resume text area with characters validation
            resume_input = ui.textarea(
                label='Resume Content',
                value=state.resume_text,
                on_change=lambda e: [setattr(state, 'resume_text', e.value), update_counters()]
            ).classes('w-full mt-2').props('outlined autogrow')
            
            resume_char_lbl = ui.label('').classes('char-counter self-end')

    # 2. Middle Section: Interview Response & Signals
    with ui.column().classes('w-full lg:w-[35%] gap-6'):
        with ui.card().classes('w-full glass-panel p-5'):
            ui.label('Interview Response').classes('text-lg font-bold text-slate-800 mb-3')
            
            question_input = ui.input(
                label='Interview Question Expected',
                value=state.question,
                on_change=lambda e: setattr(state, 'question', e.value)
            ).classes('w-full').props('outlined dense')
            
            expected_skill_input = ui.input(
                label='Expected Skill Metric',
                value=state.expected_skill,
                on_change=lambda e: setattr(state, 'expected_skill', e.value)
            ).classes('w-full mt-2').props('outlined dense')
            
            # Answer input with characters count and validation
            answer_input = ui.textarea(
                label='Candidate Transcribed Answer',
                value=state.answer_text,
                on_change=lambda e: [setattr(state, 'answer_text', e.value), update_counters()]
            ).classes('w-full mt-2').props('outlined autogrow')
            
            answer_char_lbl = ui.label('').classes('char-counter self-end')

        # Video Observation Flags Card (Interactive checkboxes)
        with ui.card().classes('w-full glass-panel p-5'):
            ui.label('Video Observation Flags').classes('text-lg font-bold text-slate-800 mb-2')
            ui.label('Select abnormalities reported by local biometric sensors:').classes('text-xs text-slate-500 mb-4')
            
            flags_list = [
                ("lip_sync_error", "Lip-Sync Desynchronization (Critical)"),
                ("audio_unsynced", "Audio/Video Stream Latency (Critical)"),
                ("multiple_voices", "Multiple Voices Detected (Critical)"),
                ("unnatural_blink", "Unnatural Blink Frequency (Warning)"),
                ("background_swapped", "Background Overlay Detected (Warning)"),
                ("head_movement_unnatural", "Unnatural Head Movements (Warning)")
            ]
            
            checkboxes = {}
            
            def make_flag_change_handler(flag_name):
                return lambda e: flag_changed(flag_name, e.value)

            def flag_changed(flag_name, is_checked):
                if is_checked:
                    state.observation_flags.add(flag_name)
                else:
                    state.observation_flags.discard(flag_name)
                trigger_analysis()

            for flag_code, flag_desc in flags_list:
                is_initially_checked = flag_code in state.observation_flags
                checkboxes[flag_code] = ui.checkbox(
                    text=flag_desc,
                    value=is_initially_checked,
                    on_change=make_flag_change_handler(flag_code)
                ).classes('text-sm text-slate-700 my-0.5')

    # 3. Right Section: Assessment Output Dashboard
    with ui.column().classes('w-full lg:w-[28%] gap-6'):
        with ui.card().classes('w-full glass-panel p-6 items-center text-center relative overflow-hidden'):
            # Assessment Header
            ui.label('Risk Assessment').classes('text-xl font-bold text-slate-800 mb-4 self-start')
            
            # Radial / circular dial wrapper (Custom CSS)
            dial_container = ui.column().classes('items-center justify-center rounded-full w-40 h-40 p-4 mb-4')
            with dial_container:
                # Radial circular score
                score_label = ui.label('0').classes('text-4xl font-extrabold text-slate-800')
                ui.label('RISK SCORE').classes('text-[10px] tracking-widest text-slate-500 font-bold')
            
            # Badge Label
            risk_badge = ui.label('LOW RISK').classes('px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-6')
            
            # Evaluate Action Button
            action_btn = ui.button(
                'Evaluate Risk Score', 
                color='primary',
                on_click=lambda: trigger_analysis()
            ).classes('w-full font-bold py-2.5 rounded-lg shadow-sm text-white')
            
            ui.label('Updates dynamically on flag/preset modifications.').classes('text-[10px] text-slate-400 mt-2')

        # Analysis Findings/Reasons Panel
        with ui.card().classes('w-full glass-panel p-5'):
            ui.label('Scoring Findings').classes('text-lg font-bold text-slate-800 mb-3')
            
            # Container for dynamic reasons
            reasons_container = ui.column().classes('w-full gap-2')

# Footer Disclaimer (Mandatory)
with ui.row().classes('w-full justify-center mt-8 mb-12 px-6'):
    with ui.card().classes('w-full max-w-[95%] glass-panel py-4 px-6 items-center bg-blue-50/50'):
        with ui.row().classes('items-center gap-3 justify-center text-center'):
            ui.icon('info', size='sm', color='slate-500')
            ui.label(
                "Disclaimer: This score supports interviewer review and does not make a hiring decision."
            ).classes('text-xs font-medium text-slate-600')


# Helper function to refresh inputs on preset changes
def refresh_all_inputs():
    candidate_name_input.value = state.candidate_name
    claimed_skills_input.value = state.claimed_skills_str
    resume_input.value = state.resume_text
    question_input.value = state.question
    expected_skill_input.value = state.expected_skill
    answer_input.value = state.answer_text
    
    # Toggle correct checkboxes
    for flag_code, cb in checkboxes.items():
        cb.value = flag_code in state.observation_flags
        
    update_counters()

# Helper function to update character limit labels
def update_counters():
    resume_len = len(state.resume_text or "")
    answer_len = len(state.answer_text or "")
    
    resume_char_lbl.text = f"{resume_len} / 5000 chars"
    answer_char_lbl.text = f"{answer_len} / 5000 chars"
    
    # Color text red if it exceeds limits
    if resume_len > 5000:
        resume_char_lbl.classes(replace='text-red-500 font-bold')
    else:
        resume_char_lbl.classes(replace='text-slate-500')
        
    if answer_len > 5000:
        answer_char_lbl.classes(replace='text-red-500 font-bold')
    else:
        answer_char_lbl.classes(replace='text-slate-500')

# Analysis Trigger and UI Rendering Logic
def trigger_analysis():
    # Build models from input
    profile = CandidateProfile(
        candidate_id=state.candidate_id or "CAN-000",
        name=state.candidate_name or "Unknown Candidate",
        claimed_skills=[s.strip() for s in state.claimed_skills_str.split(",") if s.strip()],
        resume_text=state.resume_text or ""
    )
    
    response = InterviewResponse(
        candidate_id=state.candidate_id or "CAN-000",
        question=state.question or "",
        expected_skill=state.expected_skill or "",
        answer_text=state.answer_text or "",
        observation_flags=list(state.observation_flags)
    )
    
    # Execute scoring logic
    assessment: RiskAssessment = calculate_risk(profile, response)
    
    # Update state fields
    state.risk_score = assessment.score
    state.risk_label = assessment.risk_label
    state.risk_reasons = assessment.reasons
    
    # Update UI controls
    score_label.text = str(state.risk_score)
    risk_badge.text = f"{state.risk_label} RISK"
    
    # Apply theme based on Risk Level (Low/Medium/High)
    dial_container.classes(remove='dial-low dial-medium dial-high')
    risk_badge.classes(remove='badge-low badge-medium badge-high')
    
    if state.risk_label == "Low":
        dial_container.classes(add='dial-low')
        risk_badge.classes(add='badge-low')
    elif state.risk_label == "Medium":
        dial_container.classes(add='dial-medium')
        risk_badge.classes(add='badge-medium')
    else:
        dial_container.classes(add='dial-high')
        risk_badge.classes(add='badge-high')
        
    # Re-draw findings list
    reasons_container.clear()
    with reasons_container:
        for idx, reason in enumerate(state.risk_reasons):
            with ui.row().classes('items-center w-full gap-2 px-1'):
                # Determine icon/color for reason bullet points
                if "critical" in reason.lower() or "ai helper" in reason.lower() or "exceeded" in reason.lower() or "missing" in reason.lower():
                    ui.icon('error', size='xs', color='red-500')
                    text_cls = 'text-xs text-red-700 font-semibold'
                elif "warning" in reason.lower() or "low" in reason.lower() or "short" in reason.lower() or "empty" in reason.lower():
                    ui.icon('warning', size='xs', color='amber-500')
                    text_cls = 'text-xs text-amber-700 font-medium'
                else:
                    ui.icon('check_circle', size='xs', color='green-500')
                    text_cls = 'text-xs text-green-700'
                    
                ui.label(reason).classes(text_cls)

# Run initial calculations and update count displays
update_counters()
trigger_analysis()

# Start application (offline host and fixed ports/hot reload)
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Crextio Deepfake Guard", port=8080, reload=True, show=False)
