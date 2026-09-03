from __future__ import annotations

from dataclasses import dataclass

from simulator.reason_codes import ReasonCode

from .llm_fallback import LLMTimeoutError, classify_via_llm
from .llm_fallback import LLMClassification, LLMTimeoutError, classify_via_llm
from .reason_lookup import RULE_CONFIDENCE, bucket_for_reason_code, reasoning_for_reason_code

CONFIDENCE_THRESHOLD = 0.5


@dataclass
class ClassificationResult:
    customer_id: str
    timestamp: str
    amount: float
    reason_code_raw: str
    bucket: str
    confidence: float
    source: str  # "llm" | "rule_fallback"
    reasoning: str
    flagged_for_human_review: bool


def classify_event(event: dict, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> ClassificationResult:
    """LLM-first. Rule table is used ONLY if the LLM call times out/fails."""
    raw_code = event["reason_code"]
    text_for_llm = event.get("raw_text") or raw_code

    try:
        r = classify_via_llm(text_for_llm)
        bucket, confidence, reasoning, source = r.bucket, r.confidence, r.reasoning, "llm"
    except LLMTimeoutError:
        try:
            code = ReasonCode(raw_code)
            bucket = bucket_for_reason_code(code)
            reasoning = reasoning_for_reason_code(code) + " [LLM timeout -> rule fallback]"
        except ValueError:
            bucket = "UNCERTAIN"
            reasoning = "Unrecognised code, LLM unavailable [LLM timeout -> rule fallback]"
        confidence = RULE_CONFIDENCE
        source = "rule_fallback"

    flagged = confidence < confidence_threshold
    if flagged:
        bucket = "UNCERTAIN"
        reasoning = f"{reasoning} [confidence {confidence:.2f} below threshold -> human review]"

    return ClassificationResult(
        customer_id=event["customer_id"], timestamp=event["timestamp"], amount=event["amount"],
        reason_code_raw=raw_code, bucket=bucket, confidence=confidence, source=source,
        reasoning=reasoning, flagged_for_human_review=flagged,
    )


def classify_batch(events: list[dict], confidence_threshold: float = CONFIDENCE_THRESHOLD) -> list[ClassificationResult]:
    return [classify_event(e, confidence_threshold) for e in events]


def summarize(results: list[ClassificationResult]) -> dict:
    from collections import Counter
    return {
        "total": len(results),
        "by_bucket": dict(Counter(r.bucket for r in results)),
        "by_source": dict(Counter(r.source for r in results)),
        "flagged_for_human_review": sum(1 for r in results if r.flagged_for_human_review),
    }