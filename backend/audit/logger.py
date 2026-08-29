"""
audit/logger.py

Thin write-only helpers that turn objects the classification, policy,
and backtest layers ALREADY produced into AuditLogEntry rows. This
module never re-derives or re-judges a decision — it only records ones
made elsewhere, verbatim, so the audit trail can never disagree with the
system's actual behaviour. If a number here looks wrong, the bug is
upstream, not in the logger.

Call sites (typical):
    classification.classifier.classify_event()  -> log_classification()
    policy.policy_engine.decide_event()          -> log_policy_decision()
    backtest.backtest.run_backtest()             -> log_backtest_run()
"""

from __future__ import annotations

from datetime import date

from .models import AuditLogEntry


def _as_date_or_none(value) -> date | None:
    if value is None:
        return None
    return value if isinstance(value, date) else date.fromisoformat(value)


def log_classification(result) -> AuditLogEntry:
    """`result` is a classification.classifier.ClassificationResult."""
    return AuditLogEntry.objects.create(
        customer_id=result.customer_id,
        event_timestamp=_as_date_or_none(result.timestamp),
        stage="classification",
        bucket=result.bucket,
        reason_code=result.reason_code_raw,
        decision_summary=f"{result.reason_code_raw} -> {result.bucket} (conf={result.confidence:.2f}, {result.source})",
        reasoning=result.reasoning,
        payload={
            "confidence": result.confidence,
            "source": result.source,
            "flagged_for_human_review": result.flagged_for_human_review,
            "amount": result.amount,
        },
    )


def log_policy_decision(decision) -> list[AuditLogEntry]:
    """
    `decision` is a policy.policy_engine.PolicyDecision. A single decision
    can represent up to three sub-decisions — EV gate (always), retry
    timing (only if EV-approved), bank-pattern adjustment (only if it
    actually moved the date) — each gets its own row.
    """
    entries = [
        AuditLogEntry.objects.create(
            customer_id=decision.customer_id,
            event_timestamp=decision.timestamp,
            stage="ev_gate",
            bucket=decision.bucket.value,
            reason_code=decision.reason_code,
            decision_summary=(
                "HARD - no retry" if decision.ev_decision.forced_no_retry
                else ("retry approved" if decision.ev_decision.should_retry else "EV <= 0 - skip")
            ),
            reasoning=decision.ev_decision.notes,
            payload={
                "p_recover": decision.ev_decision.p_recover,
                "expected_value": decision.ev_decision.expected_value,
                "retry_cost": decision.ev_decision.retry_cost,
                "amount": decision.amount,
            },
        )
    ]

    if decision.timing_decision is not None:
        entries.append(
            AuditLogEntry.objects.create(
                customer_id=decision.customer_id,
                event_timestamp=decision.timestamp,
                stage="retry_timing",
                bucket=decision.bucket.value,
                reason_code=decision.reason_code,
                decision_summary=f"suggested {decision.timing_decision.suggested_retry_date} ({decision.timing_decision.source})",
                reasoning=decision.timing_decision.notes,
                payload={
                    "delay_days": decision.timing_decision.delay_days,
                    "source": decision.timing_decision.source,
                },
            )
        )

    if decision.bank_adjusted:
        bank_note = next((line for line in decision.audit_trail if "Bank pattern" in line), "")
        entries.append(
            AuditLogEntry.objects.create(
                customer_id=decision.customer_id,
                event_timestamp=decision.timestamp,
                stage="bank_pattern",
                bucket=decision.bucket.value,
                reason_code=decision.reason_code,
                decision_summary=(
                    f"{decision.bank} flagged — pushed {decision.bank_adjustment_days} day(s) "
                    f"to {decision.final_retry_date}"
                ),
                reasoning=bank_note,
                payload={
                    "bank": decision.bank,
                    "bank_adjustment_days": decision.bank_adjustment_days,
                    "final_retry_date": str(decision.final_retry_date),
                },
            )
        )

    return entries


def log_backtest_run(report) -> AuditLogEntry:
    """`report` is a backtest.backtest.BacktestReport."""
    return AuditLogEntry.objects.create(
        customer_id="",
        event_timestamp=None,
        stage="backtest",
        bucket="",
        reason_code="",
        decision_summary=(
            f"seed={report.seed}: policy recovered ₹{report.policy.rupees_recovered:,.2f} vs "
            f"naive ₹{report.naive.rupees_recovered:,.2f} "
            f"({report.useless_retries_avoided_pct:.1f}% useless retries avoided)"
        ),
        reasoning="\n".join(report.notes),
        payload={
            "seed": report.seed,
            "total_failures": report.total_failures,
            "hard_declines_skipped": report.hard_declines_skipped,
            "policy": {
                "attempts": report.policy.attempts,
                "successes": report.policy.successes,
                "rupees_recovered": report.policy.rupees_recovered,
                "retry_cost_spent": report.policy.retry_cost_spent,
            },
            "naive": {
                "attempts": report.naive.attempts,
                "successes": report.naive.successes,
                "rupees_recovered": report.naive.rupees_recovered,
                "retry_cost_spent": report.naive.retry_cost_spent,
            },
            "useless_retries_avoided_pct": report.useless_retries_avoided_pct,
        },
    )