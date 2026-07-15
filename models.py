from dataclasses import dataclass

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
