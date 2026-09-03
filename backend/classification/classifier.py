"""
classifier.py
...
"""
from __future__ import annotations
from dataclasses import dataclass
from simulator.reason_codes import ReasonCode
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
    source: str
    reasoning: str
    flagged_for_human_review: bool

def _safe_llm_classify(text: str) -> LLMClassification:
    try:
        return classify_via_llm(text)
    except LLMTimeoutError as e:
        return LLMClassification("UNCERTAIN", 0.0, f"LLM unavailable ({e}) — routed to human review.")

def classify_event(event: dict, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> ClassificationResult:
    raw_code = event["reason_code"]
    try:
        code = ReasonCode(raw_code)
    except ValueError:
        llm_result = _safe_llm_classify(raw_code)
        bucket, confidence, reasoning = llm_result.bucket, llm_result.confidence, llm_result.reasoning
        source = "llm_fallback"
    else:
        bucket = bucket_for_reason_code(code)
        if code == ReasonCode.UNKNOWN_DECLINE:
            llm_result = _safe_llm_classify(event.get("raw_text") or raw_code)
            bucket, confidence, reasoning = llm_result.bucket, llm_result.confidence, llm_result.reasoning
            source = "llm_fallback"
        else:
            confidence = RULE_CONFIDENCE
            reasoning = reasoning_for_reason_code(code)
            source = "rule"
    flagged = confidence < confidence_threshold
    if flagged:
        bucket = "UNCERTAIN"
        reasoning = f"{reasoning} [confidence {confidence:.2f} below threshold -> human review]"
    return ClassificationResult(
        customer_id=event["customer_id"], timestamp=event["timestamp"], amount=event["amount"],
        reason_code_raw=raw_code, bucket=bucket, confidence=confidence, source=source,
        reasoning=reasoning, flagged_for_human_review=flagged,
    )

def classify_batch(events, confidence_threshold=CONFIDENCE_THRESHOLD):
    return [classify_event(e, confidence_threshold) for e in events]

def summarize(results):
    from collections import Counter
    return {
        "total": len(results),
        "by_bucket": dict(Counter(r.bucket for r in results)),
        "by_source": dict(Counter(r.source for r in results)),
        "flagged_for_human_review": sum(1 for r in results if r.flagged_for_human_review),
    }