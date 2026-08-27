"""
classifier.py

The Classification Layer described in problem statement section 5 & 6.

Input:  observable events exactly as simulator.generator produces them —
        {customer_id, timestamp, amount, reason_code} — nothing else.
Output: a ClassificationResult per event, bucketed HARD / SOFT / UNCERTAIN,
        with a confidence score and a one-line reasoning string, ready to
        feed the Action Center / Expected-Value Gate in the next stage.

Flow (matches 6.2 exactly):
    1. Try the rule table (reason_lookup.py) — deterministic, free,
       confidence 1.0. Handles the large majority of events.
    2. If reason_code isn't a recognised ReasonCode member (unknown /
       missing / free-text), fall back to the single LLM classifier
       (llm_fallback.py).
    3. Whatever bucket comes out of step 2, if its confidence is below
       CONFIDENCE_THRESHOLD, it is forced to UNCERTAIN and flagged for
       human review — the system does not force a decision it isn't
       confident about (per section 6.1).
"""

from __future__ import annotations

from dataclasses import dataclass

from simulator.reason_codes import ReasonCode

from .llm_fallback import classify_via_llm
from .reason_lookup import RULE_CONFIDENCE, bucket_for_reason_code, reasoning_for_reason_code

CONFIDENCE_THRESHOLD = 0.5


@dataclass
class ClassificationResult:
    customer_id: str
    timestamp: str
    amount: float
    reason_code_raw: str
    bucket: str  # "HARD" | "SOFT" | "UNCERTAIN"
    confidence: float
    source: str  # "rule" | "llm_fallback"
    reasoning: str
    flagged_for_human_review: bool


def classify_event(event: dict, confidence_threshold: float = CONFIDENCE_THRESHOLD) -> ClassificationResult:
    """
    Classifies a single observable event dict. Never looks at anything
    beyond {customer_id, timestamp, amount, reason_code} — no access to
    the simulator's hidden ground truth, by construction (this module
    never imports ground_truth.py or gateway.py).
    """
    raw_code = event["reason_code"]

    try:
        code = ReasonCode(raw_code)
    except ValueError:
        # Not a recognised structured code -> LLM fallback path.
        llm_result = classify_via_llm(raw_code)
        bucket, confidence, reasoning = llm_result.bucket, llm_result.confidence, llm_result.reasoning
        source = "llm_fallback"
    else:
        bucket = bucket_for_reason_code(code)
        confidence = RULE_CONFIDENCE
        reasoning = reasoning_for_reason_code(code)
        source = "rule"

    flagged = confidence < confidence_threshold
    if flagged:
        bucket = "UNCERTAIN"
        reasoning = f"{reasoning} [confidence {confidence:.2f} below threshold {confidence_threshold:.2f} -> routed to human review]"

    return ClassificationResult(
        customer_id=event["customer_id"],
        timestamp=event["timestamp"],
        amount=event["amount"],
        reason_code_raw=raw_code,
        bucket=bucket,
        confidence=confidence,
        source=source,
        reasoning=reasoning,
        flagged_for_human_review=flagged,
    )


def classify_batch(events: list[dict], confidence_threshold: float = CONFIDENCE_THRESHOLD) -> list[ClassificationResult]:
    return [classify_event(e, confidence_threshold) for e in events]


def summarize(results: list[ClassificationResult]) -> dict:
    """Quick aggregate view for sanity-checking a batch — bucket counts, source split, flagged count."""
    from collections import Counter

    return {
        "total": len(results),
        "by_bucket": dict(Counter(r.bucket for r in results)),
        "by_source": dict(Counter(r.source for r in results)),
        "flagged_for_human_review": sum(1 for r in results if r.flagged_for_human_review),
    }


if __name__ == "__main__":
    from simulator.generator import SyntheticDataset

    ds = SyntheticDataset(seed=42, n_customers=200, months=4)
    events = ds.observable_events_as_dicts()

    results = classify_batch(events)
    print(f"Classified {len(results)} events\n")

    print("Sample results:")
    for r in results[:5]:
        print(f"  {r.customer_id}  {r.reason_code_raw:20s} -> {r.bucket:10s} conf={r.confidence:.2f}  ({r.source})")

    print("\nSummary:")
    for k, v in summarize(results).items():
        print(f"  {k}: {v}")

    # Free-text fallback demo — a code the enum has never seen.
    weird_event = {"customer_id": "cust_99999", "timestamp": "2026-05-01", "amount": 499, "reason_code": "Card was reported blocked by issuer"}
    weird_result = classify_event(weird_event)
    print("\nFree-text fallback demo:")
    print(f"  {weird_result}")