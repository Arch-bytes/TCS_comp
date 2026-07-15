"""Transparent, local rule signals for interview-answer review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

MAX_TEXT_LENGTH = 5_000
MIN_SUBSTANTIVE_ANSWER_LENGTH = 60

# These phrases are only a lightweight demo signal.  They are never a decision.
CANNED_PHRASES = (
    "as an ai language model",
    "i cannot provide",
    "i'm unable to",
    "i am unable to",
    "my training data",
)
OBSERVATION_FLAG_PENALTIES = {
    "inconsistent": 15,
    "off_topic": 15,
    "scripted": 15,
    "verification_needed": 10,
}


@dataclass(frozen=True)
class RuleSignal:
    """A bounded risk contribution with reviewer-facing plain-language reason."""

    penalty: int
    reason: str


def normalize_text(value: object, *, limit: int = MAX_TEXT_LENGTH) -> str | None:
    """Return trimmed text, or None when it is absent, non-text, or oversized."""
    if not isinstance(value, str) or len(value) > limit:
        return None
    return " ".join(value.split())


def evaluate_response(response: object) -> list[RuleSignal]:
    """Evaluate answer-depth, canned-language, and supplied observation signals.

    The function intentionally accepts an object rather than a concrete dataclass so
    it stays safe at the UI boundary; malformed values simply yield no rule signal.
    """
    answer = normalize_text(getattr(response, "answer_text", None))
    if answer is None:
        return []

    signals: list[RuleSignal] = []
    lower_answer = answer.casefold()
    if len(answer) < MIN_SUBSTANTIVE_ANSWER_LENGTH:
        signals.append(RuleSignal(25, "Answer is too brief to demonstrate depth."))
    if any(phrase in lower_answer for phrase in CANNED_PHRASES):
        signals.append(RuleSignal(20, "Answer contains a canned-response phrase."))

    raw_flags = getattr(response, "observation_flags", [])
    if isinstance(raw_flags, Iterable) and not isinstance(raw_flags, (str, bytes)):
        matched_flags = {
            flag.strip().casefold()
            for flag in raw_flags
            if isinstance(flag, str) and flag.strip().casefold() in OBSERVATION_FLAG_PENALTIES
        }
        flag_penalty = min(30, sum(OBSERVATION_FLAG_PENALTIES[flag] for flag in matched_flags))
        if flag_penalty:
            signals.append(
                RuleSignal(flag_penalty, "Interviewer observation flags require follow-up review.")
            )
    return signals
