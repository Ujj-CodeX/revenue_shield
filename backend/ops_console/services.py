"""
ops_console/services.py

Wires the whole pipeline together for the merchant dashboard:
    simulator.generator -> classification.classifier -> policy.policy_engine
    -> backtest.backtest (for the measured policy-vs-naive numbers)
and shapes the result into the JSON the Vue frontend (src/data/mockData.js
shape) renders. This is the one place all five apps meet — it deliberately
contains no decision logic of its own, only orchestration + formatting.
"""

from __future__ import annotations

from classification.classifier import classify_batch
from policy.bank_pattern_detection import detect_systemic_days
from policy.policy_engine import decide_batch
from simulator.generator import SyntheticDataset

from backtest.backtest import DEFAULT_RETRY_COST, persist_backtest_run, run_backtest


def _status_and_retry_date(decision) -> tuple[str, str]:
    if decision.ev_decision.forced_no_retry:
        return "NO RETRY", "-"
    if decision.final_retry_date is None:
        return "NO RETRY", "-"
    return "RETRY RECOMMENDED", decision.final_retry_date.isoformat()


def build_dashboard_payload(seed: int = 42, n_customers: int = 200, months: int = 4, persist: bool = True) -> dict:
    ds = SyntheticDataset(seed=seed, n_customers=n_customers, months=months)
    events = ds.observable_events_as_dicts()

    classifications = classify_batch(events)
    systemic_flags = detect_systemic_days(events)
    decisions = decide_batch(events, classifications, systemic_flags=systemic_flags, retry_cost=DEFAULT_RETRY_COST)

    report = run_backtest(seed=seed, n_customers=n_customers, months=months)
    run = persist_backtest_run(report, n_customers=n_customers, months=months) if persist else None

    recoverable = sum(
        d.ev_decision.expected_value for d in decisions if d.ev_decision.should_retry
    )
    revenue_at_risk = sum(d.amount for d in decisions)
    recovered = report.policy.rupees_recovered
    recovery_rate = (recovered / recoverable * 100.0) if recoverable else 0.0

    kpi_metrics = {
        "revenueAtRisk": round(revenue_at_risk, 2),
        "revenueAtRiskSubtitle": f"Across {len(decisions)} failed payments",
        "recoverableRevenue": round(recoverable, 2),
        "recoverableRevenueSubtitle": "Expected from EV-positive retries",
        "recoveryRate": round(recovery_rate, 1),
        "recoveryRateSubtitle": "(Recovered / Recoverable)",
        "uselessRetriesAvoided": report.naive.useless_retries - report.policy.useless_retries,
        "uselessRetriesAvoidedSubtitle": "Vs naive retry everything",
    }

    failed_payments = []
    for d in decisions:
        status, retry_date = _status_and_retry_date(d)
        failed_payments.append({
            "customerId": d.customer_id,
            "reasonCode": d.reason_code,
            "bucket": d.bucket.value,
            "confidence": round(d.confidence, 2),
            "retryDate": retry_date,
            "status": status,
            "expectedRecovery": round(max(d.ev_decision.expected_value, 0.0), 2),
        })

    return {
        "merchantContext": {
            "seed": seed,
            "backtestRunId": f"BT_run_{run.id}" if run else None,
            "totalFailures": report.total_failures,
        },
        "kpiMetrics": kpi_metrics,
        "failedPaymentsData": failed_payments,
        "backtest": {
            "policy": {
                "attempts": report.policy.attempts,
                "successes": report.policy.successes,
                "recovered": report.policy.rupees_recovered,
                "net": report.policy.rupees_recovered - report.policy.retry_cost_spent,
            },
            "naive": {
                "attempts": report.naive.attempts,
                "successes": report.naive.successes,
                "recovered": report.naive.rupees_recovered,
                "net": report.naive.rupees_recovered - report.naive.retry_cost_spent,
            },
            "uselessRetriesAvoidedPct": round(report.useless_retries_avoided_pct, 1),
            "notes": report.notes,
        },
    }