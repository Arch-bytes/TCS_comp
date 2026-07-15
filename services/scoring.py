from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models import CandidateProfile, InterviewResponse, RiskAssessment

MAX_INPUT_LENGTH = 3000
_GENERIC_PATTERNS = (
    r"\bas\s+an\s+ai\b",
    r"\blanguage\s+model\b",
    r"\bopenai\b",
    r"\bchatgpt\b",
    r"\bmy\s+knowledge\s+cutoff\b",
    r"\bgenerated\s+by\s+ai\b",
    r"\bi\s+cannot\s+provide\b",
)
_CRITICAL_FLAGS = {"multiple_voices", "lip_sync_error", "audio_unsynced"}
_WARNING_FLAGS = {"unnatural_blink", "background_swapped", "head_movement_unnatural"}


def _low_confidence(candidate_id: str, message: str) -> RiskAssessment:
    return RiskAssessment(
        candidate_id=candidate_id or "UNKNOWN",
        score=0,
        risk_label="Low",
        reasons=[f"Low-confidence error: {message}"],
    )


def _clean_text(text: str | None) -> str:
    return (text or "").strip()


def _text_similarity(left: str, right: str) -> float:
    left_text = _clean_text(left)
    right_text = _clean_text(right)
    if not left_text or not right_text:
        return 0.0
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = vectorizer.fit_transform([left_text, right_text])
        return float(cosine_similarity(matrix[0], matrix[1])[0, 0])
    except ValueError:
        return 0.0


def _skill_coverage(claimed_skills: list[str], answer_text: str) -> float:
    if not claimed_skills:
        return 0.0
    lowered_answer = answer_text.lower()
    hits = 0
    for skill in claimed_skills:
        normalized_skill = skill.lower().strip()
        if normalized_skill and normalized_skill in lowered_answer:
            hits += 1
    return hits / len(claimed_skills)


def _has_generic_phrase(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in _GENERIC_PATTERNS)


def score_candidate(profile: CandidateProfile, response: InterviewResponse) -> RiskAssessment:
    candidate_id = _clean_text(profile.candidate_id) or "UNKNOWN"
    candidate_name = _clean_text(profile.name)
    resume_text = _clean_text(profile.resume_text)
    answer_text = _clean_text(response.answer_text)
    claimed_skills = [skill.strip() for skill in profile.claimed_skills if skill and skill.strip()]

    if len(candidate_name) == 0:
        return _low_confidence(candidate_id, "missing candidate name")
    if not claimed_skills:
        return _low_confidence(candidate_id, "missing claimed skills")
    if len(resume_text) == 0:
        return _low_confidence(candidate_id, "missing resume text")
    if len(answer_text) == 0:
        return _low_confidence(candidate_id, "missing answer text")
    if len(resume_text) > MAX_INPUT_LENGTH or len(answer_text) > MAX_INPUT_LENGTH:
        return _low_confidence(candidate_id, f"input exceeded {MAX_INPUT_LENGTH} characters")

    claimed_text = " ".join(claimed_skills)
    overall_similarity = _text_similarity(f"{resume_text} {claimed_text}", answer_text)
    resume_similarity = _text_similarity(resume_text, answer_text)
    skill_coverage = _skill_coverage(claimed_skills, answer_text)

    support = (overall_similarity * 0.30) + (resume_similarity * 0.20) + (skill_coverage * 0.50)
    score = round((1.0 - support) * 55)
    reasons: list[str] = []

    if overall_similarity < 0.08:
        score += 8
        reasons.append(f"Low TF-IDF overlap with the resume and skill summary ({overall_similarity:.0%})")
    elif overall_similarity < 0.18:
        score += 4
        reasons.append(f"Moderate TF-IDF overlap with the resume and skill summary ({overall_similarity:.0%})")

    if skill_coverage < 0.34:
        score += 12
        reasons.append("The answer does not meaningfully reference the claimed skills")

    if response.expected_skill and _text_similarity(response.expected_skill, answer_text) < 0.10:
        score += 8
        reasons.append(f"Expected skill '{response.expected_skill}' is not clearly supported in the answer")

    word_count = len(re.findall(r"\b\w+\b", answer_text))
    if word_count < 20:
        score += 12
        reasons.append("Answer depth is very short for an interview response")

    if _has_generic_phrase(answer_text):
        score += 30
        reasons.append("Generic or canned assistant phrasing detected in the answer")

    flag_penalty = 0
    for flag in response.observation_flags or []:
        normalized_flag = flag.lower().strip()
        if normalized_flag in _CRITICAL_FLAGS:
            flag_penalty += 18
            reasons.append(f"Critical manual observation note: {flag}")
        elif normalized_flag in _WARNING_FLAGS:
            flag_penalty += 8
            reasons.append(f"Warning manual observation note: {flag}")

    score += min(flag_penalty, 40)
    score = max(0, min(score, 100))

    if score >= 70:
        risk_label = "High"
    elif score >= 30:
        risk_label = "Medium"
    else:
        risk_label = "Low"

    if not reasons:
        reasons.append("Text signals look broadly consistent with the claimed interview profile.")

    return RiskAssessment(
        candidate_id=candidate_id,
        score=score,
        risk_label=risk_label,
        reasons=reasons,
    )


calculate_risk = score_candidate
