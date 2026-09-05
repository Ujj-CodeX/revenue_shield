

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Bucket(str, Enum):
    HARD = "HARD"
    SOFT = "SOFT"
    UNCERTAIN = "UNCERTAIN"



BUCKET_BASE_RECOVERY_RATE: dict[Bucket, float] = {
    Bucket.HARD: 0.0,      
    Bucket.SOFT: 0.55,      
    Bucket.UNCERTAIN: 0.30, 
}


REASON_RECOVERY_RATE_OVERRIDE: dict[str, float] = {
    "INSUFFICIENT_FUNDS": 0.60,
    "BANK_TIMEOUT": 0.70,
    "NETWORK_ERROR": 0.75,
}

DEFAULT_RETRY_COST = 2.0  # flat simulated cost per retry attempt (gateway fee)


@dataclass
class EVDecision:
    reason_code: str
    bucket: Bucket
    amount: float
    p_recover: float
    retry_cost: float
    expected_value: float
    should_retry: bool
    forced_no_retry: bool  # True only when the HARD-bucket rule overrides the math
    notes: str


def estimate_recovery_probability(reason_code: str, bucket: Bucket, confidence: float) -> float:
    
    if bucket == Bucket.HARD:
        return 0.0
    if bucket == Bucket.SOFT:
        return REASON_RECOVERY_RATE_OVERRIDE.get(reason_code, BUCKET_BASE_RECOVERY_RATE[Bucket.SOFT])
    if bucket == Bucket.UNCERTAIN:
        return BUCKET_BASE_RECOVERY_RATE[Bucket.UNCERTAIN] * confidence
    raise ValueError(f"Unknown bucket: {bucket!r}")


def evaluate(
    reason_code: str,
    bucket: Bucket,
    confidence: float,
    amount: float,
    retry_cost: float = DEFAULT_RETRY_COST,
) -> EVDecision:
   
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if not (0.0 <= confidence <= 1.0):
        raise ValueError("confidence must be in [0, 1]")

    # Design rule 1: HARD is a hard stop, independent of the EV number.
    if bucket == Bucket.HARD:
        return EVDecision(
            reason_code=reason_code,
            bucket=bucket,
            amount=amount,
            p_recover=0.0,
            retry_cost=retry_cost,
            expected_value=-retry_cost,
            should_retry=False,
            forced_no_retry=True,
            notes="HARD decline: customer/bank-side action required. Not an EV call — retries are disabled by rule.",
        )

    p_recover = estimate_recovery_probability(reason_code, bucket, confidence)
    ev = p_recover * amount - retry_cost
    should_retry = ev > 0

    return EVDecision(
        reason_code=reason_code,
        bucket=bucket,
        amount=amount,
        p_recover=p_recover,
        retry_cost=retry_cost,
        expected_value=ev,
        should_retry=should_retry,
        forced_no_retry=False,
        notes=(
            f"EV = {p_recover:.2f} * {amount:.2f} - {retry_cost:.2f} = {ev:.2f} "
            f"-> {'retry' if should_retry else 'do not retry'}"
        ),
    )


def evaluate_batch(events: list[dict], retry_cost: float = DEFAULT_RETRY_COST) -> list[EVDecision]:
    
    decisions = []
    for e in events:
        decisions.append(
            evaluate(
                reason_code=e["reason_code"],
                bucket=Bucket(e["bucket"]),
                confidence=e["confidence"],
                amount=e["amount"],
                retry_cost=retry_cost,
            )
        )
    return decisions


if __name__ == "__main__":
    demo_events = [
        {"reason_code": "CARD_EXPIRED", "bucket": "HARD", "confidence": 1.0, "amount": 999},
        {"reason_code": "INSUFFICIENT_FUNDS", "bucket": "SOFT", "confidence": 1.0, "amount": 499},
        {"reason_code": "NETWORK_ERROR", "bucket": "SOFT", "confidence": 1.0, "amount": 199},
        {"reason_code": "UNKNOWN_DECLINE", "bucket": "UNCERTAIN", "confidence": 0.4, "amount": 1499},
        {"reason_code": "UNKNOWN_DECLINE", "bucket": "UNCERTAIN", "confidence": 0.9, "amount": 1499},
    ]
    for d in evaluate_batch(demo_events):
        print(f"{d.reason_code:20s} bucket={d.bucket.value:10s} amount={d.amount:7.2f} -> {d.notes}")