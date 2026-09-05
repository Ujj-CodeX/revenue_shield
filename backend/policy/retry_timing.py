

from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import date, timedelta

from policy.ev_gate import Bucket


REASON_DEFAULT_RETRY_DELAY_DAYS: dict[str, int] = {
    "NETWORK_ERROR": 0,       
    "BANK_TIMEOUT": 1,        
    "INSUFFICIENT_FUNDS": 3,   
}



BUCKET_FALLBACK_RETRY_DELAY_DAYS: dict[Bucket, int] = {
    Bucket.SOFT: 2,
    Bucket.UNCERTAIN: 2,
}

MAX_HISTORY_POINTS_USED = 10  


@dataclass
class RetryTimingDecision:
    reason_code: str
    bucket: Bucket
    original_failure_date: date
    suggested_retry_date: date
    delay_days: int
    source: str  
    notes: str


def _delay_from_history(retry_success_offsets_days: list[int]) -> int | None:
   
    if not retry_success_offsets_days:
        return None
    recent = retry_success_offsets_days[-MAX_HISTORY_POINTS_USED:]
    return round(statistics.median(recent))


def suggest_retry_date(
    reason_code: str,
    bucket: Bucket,
    original_failure_date: date,
    customer_retry_success_history_days: list[int] | None = None,
) -> RetryTimingDecision:
    
    if bucket == Bucket.HARD:
        raise ValueError("retry_timing should never be called on a HARD-bucket event")

    history_delay = _delay_from_history(customer_retry_success_history_days or [])
    if history_delay is not None:
        delay_days = history_delay
        source = "customer_history"
        notes = (
            f"Used median of this customer's own past retry-success offsets "
            f"({len(customer_retry_success_history_days)} data point(s)) -> {delay_days} day(s)."
        )
    elif reason_code in REASON_DEFAULT_RETRY_DELAY_DAYS:
        delay_days = REASON_DEFAULT_RETRY_DELAY_DAYS[reason_code]
        source = "reason_default"
        notes = f"No customer history yet; used the {reason_code} default window -> {delay_days} day(s)."
    else:
        delay_days = BUCKET_FALLBACK_RETRY_DELAY_DAYS.get(bucket, 2)
        source = "bucket_fallback"
        notes = f"No customer history or reason-specific default; used {bucket.value} bucket fallback -> {delay_days} day(s)."

    return RetryTimingDecision(
        reason_code=reason_code,
        bucket=bucket,
        original_failure_date=original_failure_date,
        suggested_retry_date=original_failure_date + timedelta(days=delay_days),
        delay_days=delay_days,
        source=source,
        notes=notes,
    )


if __name__ == "__main__":
    today = date(2026, 3, 15)

    print("No history (reason default):")
    d1 = suggest_retry_date("INSUFFICIENT_FUNDS", Bucket.SOFT, today)
    print(" ", d1.notes, "->", d1.suggested_retry_date)

    print("\nWith customer history (retries succeeded at day 5, 4, 6 previously):")
    d2 = suggest_retry_date("INSUFFICIENT_FUNDS", Bucket.SOFT, today, customer_retry_success_history_days=[5, 4, 6])
    print(" ", d2.notes, "->", d2.suggested_retry_date)

    print("\nNETWORK_ERROR, no history (fast default):")
    d3 = suggest_retry_date("NETWORK_ERROR", Bucket.SOFT, today)
    print(" ", d3.notes, "->", d3.suggested_retry_date)

    print("\nUNCERTAIN bucket, unknown reason, no history (bucket fallback):")
    d4 = suggest_retry_date("UNKNOWN_DECLINE", Bucket.UNCERTAIN, today)
    print(" ", d4.notes, "->", d4.suggested_retry_date)