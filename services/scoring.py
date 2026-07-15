"""
Main risk scoring coordination engine.
"""

import logging
from statistics import fmean
from models import CandidateProfile, InterviewResponse, RiskAssessment
from . import config
from .nlp_match import (
    clean_text,
    get_text_similarity,
    get_skill_similarities,
    get_skill_coverage
)
from .rules import (
    has_generic_ai_phrase,
    get_word_count,
    evaluate_behavioral_flags
)

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = config.MAX_INPUT_LENGTH

def _low_confidence(candidate_id: str, message: str) -> RiskAssessment:
    """Return a default low-confidence result when validation fails."""
    logger.error(f"Low confidence assessment for {candidate_id}: {message}")
    return RiskAssessment(
        candidate_id=candidate_id or "UNKNOWN",
        score=0,
        risk_label="Low",
        reasons=[f"Low-confidence error: {message}"],
    )

def score_candidate(profile: CandidateProfile, response: InterviewResponse) -> RiskAssessment:
    """
    Evaluates a candidate's interview response against their profile to calculate an impersonation risk score.
    """
    # 1. Validation and Sanitization
    candidate_id = clean_text(profile.candidate_id) or "UNKNOWN"
    candidate_name = clean_text(profile.name)
    resume_text = clean_text(profile.resume_text)
    answer_text = clean_text(response.answer_text)
    claimed_skills = [skill.strip() for skill in profile.claimed_skills if skill and skill.strip()]

    if not candidate_name:
        return _low_confidence(candidate_id, "missing candidate name")
    if not claimed_skills:
        return _low_confidence(candidate_id, "missing claimed skills")
    if not resume_text:
        return _low_confidence(candidate_id, "missing resume text")
    if not answer_text:
        return _low_confidence(candidate_id, "missing answer text")
    if len(resume_text) > config.MAX_INPUT_LENGTH or len(answer_text) > config.MAX_INPUT_LENGTH:
        return _low_confidence(candidate_id, f"input exceeded {config.MAX_INPUT_LENGTH} characters")

    logger.info(f"Scoring candidate: {candidate_name} ({candidate_id})")

    # 2. NLP Feature Extraction
    claimed_text = " ".join(claimed_skills)
    overall_similarity = get_text_similarity(f"{resume_text} {claimed_text}", answer_text)
    resume_similarity = get_text_similarity(resume_text, answer_text)
    skill_pairs = get_skill_similarities(claimed_skills, answer_text)
    skill_coverage = get_skill_coverage(claimed_skills, answer_text)
    skill_strength = fmean(similarity for _, similarity in skill_pairs) if skill_pairs else 0.0
    word_count = get_word_count(answer_text)

    # 3. Base Support Calculation
    # Support represents how much evidence we have that the candidate is authentic.
    support = (
        (overall_similarity * config.WEIGHT_OVERALL_SIMILARITY)
        + (resume_similarity * config.WEIGHT_RESUME_SIMILARITY)
        + (skill_strength * config.WEIGHT_SKILL_STRENGTH)
        + (skill_coverage * config.WEIGHT_SKILL_COVERAGE)
    )
    
    # Invert support to get base risk score
    score = round((1.0 - support) * config.BASE_RISK_MULTIPLIER)
    reasons: list[str] = []

    # 4. Rule-Based Penalty and Bonus Application
    
    # NLP Similarity Checks
    if overall_similarity < config.LOW_SIMILARITY_THRESHOLD:
        score += config.PENALTY_LOW_SIMILARITY
        reasons.append(f"Low TF-IDF overlap with profile ({overall_similarity:.0%})")
    elif overall_similarity < config.MODERATE_SIMILARITY_THRESHOLD:
        score += config.PENALTY_MODERATE_SIMILARITY
        reasons.append(f"Moderate TF-IDF overlap with profile ({overall_similarity:.0%})")

    # Skill Specific Checks
    if skill_pairs:
        ranked_skills = sorted(skill_pairs, key=lambda item: item[1], reverse=True)
        top_skill, top_similarity = ranked_skills[0]
        reasons.append(f"Top claimed skill match: {top_skill} ({top_similarity:.0%})")
        if len(ranked_skills) > 1:
            runner_up_skill, runner_up_similarity = ranked_skills[1]
            reasons.append(f"Runner-up skill match: {runner_up_skill} ({runner_up_similarity:.0%})")

    if skill_coverage >= config.STRONG_ALIGNMENT_COVERAGE and overall_similarity >= config.STRONG_ALIGNMENT_SIMILARITY and word_count >= config.MIN_PROFESSIONAL_WORD_COUNT:
        score -= config.BONUS_STRONG_ALIGNMENT
        reasons.append("Strong resume and skill alignment with detailed answer")
    elif skill_coverage < 0.34:
        score += config.PENALTY_WEAK_COVERAGE
        reasons.append("Answer does not meaningfully reference claimed skills")

    if skill_strength < config.WEAK_SKILL_STRENGTH_THRESHOLD:
        score += config.PENALTY_WEAK_STRENGTH
        reasons.append("Skill-to-answer similarity is consistently weak")

    # Expected Competency Check
    if response.expected_skill:
        expected_sim = get_text_similarity(response.expected_skill, answer_text)
        if expected_sim < config.LOW_SIMILARITY_THRESHOLD:
            score += config.PENALTY_EXPECTED_SKILL_MISMATCH
            reasons.append(f"Expected skill '{response.expected_skill}' not supported in answer")

    # Depth and AI Phrasing
    if word_count < config.MIN_PROFESSIONAL_WORD_COUNT:
        score += config.PENALTY_SHORT_ANSWER
        reasons.append("Answer depth is insufficient for a professional response")

    if has_generic_ai_phrase(answer_text):
        score += config.PENALTY_AI_PHRASE
        reasons.append("Generic or canned AI assistant phrasing detected")

    # Behavioral Observation Flags
    flag_penalty, flag_reasons = evaluate_behavioral_flags(response.observation_flags or [])
    score += min(flag_penalty, config.PENALTY_MAX_FLAGS)
    reasons.extend(flag_reasons)

    # Clean Profile Bonus
    if skill_coverage >= config.STRONG_ALIGNMENT_COVERAGE and not response.observation_flags and not has_generic_ai_phrase(answer_text):
        score -= config.BONUS_CLEAN_PROFILE

    # 5. Final Normalization and Labeling
    score = max(0, min(score, 100))

    if score >= config.THRESHOLD_HIGH_RISK:
        risk_label = "High"
    elif score >= config.THRESHOLD_MEDIUM_RISK:
        risk_label = "Medium"
    else:
        risk_label = "Low"

    if not reasons:
        reasons.append("Text signals look broadly consistent with the claimed profile.")

    logger.info(f"Assessment complete. Score: {score}, Label: {risk_label}")
    return RiskAssessment(
        candidate_id=candidate_id,
        score=score,
        risk_label=risk_label,
        reasons=reasons,
    )

# Alias for backward compatibility
calculate_risk = score_candidate
