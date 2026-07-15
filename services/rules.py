"""
Heuristic rules and behavioral flag evaluation for risk detection.
"""

import re
import logging
from typing import List, Set
from .config import (
    GENERIC_AI_PATTERNS,
    CRITICAL_FLAGS,
    WARNING_FLAGS,
    FLAG_PENALTY_CRITICAL,
    FLAG_PENALTY_WARNING
)

logger = logging.getLogger(__name__)

def has_generic_ai_phrase(text: str) -> bool:
    """Check if the text contains common AI assistant boilerplate phrases."""
    lowered = text.lower()
    for pattern in GENERIC_AI_PATTERNS:
        if re.search(pattern, lowered):
            logger.warning(f"AI phrase detected pattern: {pattern}")
            return True
    return False

def get_word_count(text: str) -> int:
    """Calculate the number of words in the text."""
    return len(re.findall(r"\b\w+\b", text))

def evaluate_behavioral_flags(flags: List[str]) -> tuple[int, List[str]]:
    """
    Evaluate manual observation flags and calculate total penalty.
    Returns (total_penalty, reason_messages).
    """
    penalty = 0
    reasons = []
    
    # Use set for faster lookup and to avoid duplicate penalties if flags are repeated
    seen_flags: Set[str] = set()
    
    for flag in flags:
        normalized_flag = flag.lower().strip()
        if not normalized_flag or normalized_flag in seen_flags:
            continue
            
        seen_flags.add(normalized_flag)
        
        if normalized_flag in CRITICAL_FLAGS:
            penalty += FLAG_PENALTY_CRITICAL
            reasons.append(f"Critical observation: {flag.replace('_', ' ').title()}")
            logger.warning(f"Critical flag detected: {normalized_flag}")
        elif normalized_flag in WARNING_FLAGS:
            penalty += FLAG_PENALTY_WARNING
            reasons.append(f"Behavioral warning: {flag.replace('_', ' ').title()}")
            logger.info(f"Warning flag detected: {normalized_flag}")
            
    return penalty, reasons
