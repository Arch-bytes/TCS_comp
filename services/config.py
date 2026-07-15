"""
Configuration and constants for the Risk Scoring Engine.
"""

# Text processing constraints
MAX_INPUT_LENGTH = 3000
MIN_PROFESSIONAL_WORD_COUNT = 24

# NLP Scoring Weights (Sum should ideally be 1.0 for the 'support' metric)
WEIGHT_OVERALL_SIMILARITY = 0.30
WEIGHT_RESUME_SIMILARITY = 0.15
WEIGHT_SKILL_STRENGTH = 0.20
WEIGHT_SKILL_COVERAGE = 0.35

# Scoring Multipliers and Thresholds
BASE_RISK_MULTIPLIER = 36  # (1.0 - support) * BASE_RISK_MULTIPLIER
LOW_SIMILARITY_THRESHOLD = 0.10
MODERATE_SIMILARITY_THRESHOLD = 0.20
STRONG_ALIGNMENT_SIMILARITY = 0.18
STRONG_ALIGNMENT_COVERAGE = 0.66
WEAK_SKILL_STRENGTH_THRESHOLD = 0.12

# Penalty / Bonus Values
PENALTY_LOW_SIMILARITY = 10
PENALTY_MODERATE_SIMILARITY = 5
PENALTY_WEAK_COVERAGE = 12
PENALTY_WEAK_STRENGTH = 8
PENALTY_EXPECTED_SKILL_MISMATCH = 8
PENALTY_SHORT_ANSWER = 12
PENALTY_AI_PHRASE = 30
PENALTY_MAX_FLAGS = 40

BONUS_STRONG_ALIGNMENT = 20
BONUS_CLEAN_PROFILE = 10  # Bonus if high coverage, no flags, no AI phrases

# Behavioral Flags
CRITICAL_FLAGS = {
    "multiple_voices",
    "lip_sync_error",
    "audio_unsynced",
    "prompting_detected",
    "external_assistance",
}

WARNING_FLAGS = {
    "unnatural_blink",
    "background_swapped",
    "head_movement_unnatural",
    "poor_eye_contact",
    "reading_from_script",
}

FLAG_PENALTY_CRITICAL = 18
FLAG_PENALTY_WARNING = 8

# AI Canned Phrases (Regex patterns)
GENERIC_AI_PATTERNS = (
    r"\bas\s+an\s+ai\b",
    r"\blanguage\s+model\b",
    r"\bopenai\b",
    r"\bchatgpt\b",
    r"\bmy\s+knowledge\s+cutoff\b",
    r"\bgenerated\s+by\s+ai\b",
    r"\bi\s+cannot\s+provide\b",
    r"\bi\s+am\s+an\s+ai\b",
)

# Risk Label Thresholds
THRESHOLD_HIGH_RISK = 70
THRESHOLD_MEDIUM_RISK = 30
