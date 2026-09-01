"""
ops_console/services.py

Wires the whole pipeline together for the merchant dashboard:
    simulator.generator -> classification.classifier -> policy.policy_engine
    -> backtest.backtest
and shapes it into EXACTLY the same keys/format as the frontend's former
src/data/mockData.js, so MerchantDashboard.vue needs no prop-shape changes
— only its data source changes from a static import to this endpoint.
"""

from __future__ import annotations

from datetime import date

from classification.classifier import classify_batch
from policy.bank_pattern_detection import detect_systemic_days
from policy.policy_engine import decide_batch
from simulator.generator import SyntheticDataset

from backtest.backtest import DEFAULT_RETRY_COST, persist_backtest_run, run_backtest


def _inr(n: float) -> str:
    """Indian digit grouping: ₹48,32,100 style, matching mockData.js."""
    n = round(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    s = str(n)
    if len(s) <= 3:
        grouped = s
    else:
        last3, rest = s[-3:], s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        grouped = ",".join(parts) + "," + last3
    return f"₹{sign}{grouped}"


def _pct(n: float) -> str:
    return f"{n:.1f}%"


def build_dashboard_payload(seed: int = 42, n_customers: int = 200, months: int = 4) -> dict:
    ds = SyntheticDataset(seed=seed, n_customers=n_customers, months=months)
    events = ds.observable_events_as_dicts()

    classifications = classify_batch(events)
    systemic_flags = detect_systemic_days(events)
    decisions = decide_batch(events, classifications, systemic_flags=systemic_flags, retry_cost=DEFAULT_RETRY_COST)

    report = run_backtest(seed=seed, n_customers=n_customers, months=months)
    run = persist_backtest_run(report, n_customers=n_customers, months=months)

    total = len(decisions)
    hard = [d for d in decisions if d.bucket.value == "HARD"]
    soft = [d for d in decisions if d.bucket.value == "SOFT"]
    uncertain = [d for d in decisions if d.bucket.value == "UNCERTAIN"]
    retried = [d for d in decisions if d.ev_decision.should_retry]

    revenue_at_risk = sum(d.amount for d in decisions)
    recoverable = sum(d.ev_decision.expected_value for d in retried)

    merchant_context = {
        "merchantName": "REVENUE SHIELD DEMO",
        "merchantId": f"SEED_{seed}",
        "industry": "Subscriptions",
        "plan": "Premium",
        "status": "ACTIVE",
        "onboardedDate": "-",
        "seed": seed,
        "backtestRunId": f"BT_run_{run.id}",
        "dataAsOf": date.today().strftime("%d %b %Y"),
        "dateRange": f"{n_customers} customers / {months} months",
    }

    kpi_metrics = {
        "revenueAtRisk": _inr(revenue_at_risk),
        "revenueAtRiskSubtitle": f"Across {total} failed payments",
        "recoverableRevenue": _inr(recoverable),
        "recoverableRevenueSubtitle": "Expected from EV-positive retries",
        "recoveryRate": _pct((report.policy.rupees_recovered / recoverable * 100.0) if recoverable else 0.0),
        "recoveryRateSubtitle": "(Recovered / Recoverable)",
        "uselessRetriesAvoided": str(report.naive.useless_retries - report.policy.useless_retries),
        "uselessRetriesAvoidedSubtitle": "Vs naive retry everything",
    }

    failed_payments = []
    for d in decisions[:50]:
        if d.ev_decision.forced_no_retry:
            status, retry_date, expected = "NO RETRY", "-", "₹0"
        elif not d.ev_decision.should_retry:
            status, retry_date, expected = ("MANUAL REVIEW" if d.bucket.value == "UNCERTAIN" else "NO RETRY"), "-", "-"
        else:
            status = "RETRY RECOMMENDED"
            retry_date = d.final_retry_date.strftime("%d %b %Y") if d.final_retry_date else "-"
            expected = _inr(d.ev_decision.expected_value)
        failed_payments.append({
            "customerId": d.customer_id,
            "reasonCode": d.reason_code,
            "bucket": d.bucket.value,
            "confidence": f"{d.confidence:.2f}",
            "retryDate": retry_date,
            "status": status,
            "expectedRecovery": expected,
        })

    def _pct_of(n):
        return _pct(100.0 * n / total) if total else "0.0%"

    bucket_summary = {
        "hardDeclines": {"count": str(len(hard)), "percentage": _pct_of(len(hard))},
        "softDeclines": {"count": str(len(soft)), "percentage": _pct_of(len(soft))},
        "uncertain": {"count": str(len(uncertain)), "percentage": _pct_of(len(uncertain))},
        "scheduledRetries": str(len(retried)),
        "resolvedRecovered": str(report.policy.successes),
        "resolvedNotRecovered": str(report.policy.attempts - report.policy.successes),
        "skippedByEvGate": str(len(soft) + len(uncertain) - len(retried)),
    }

    from collections import Counter
    hard_reason_counts = Counter(d.reason_code for d in hard)
    hard_decline_report = {
        "hardDeclinesCount": str(len(hard)),
        "expectedRevenueLoss": _inr(sum(d.amount for d in hard)),
        "fileName": f"hard_declines_seed{seed}.csv",
        "fileSize": "-",
        "topReasons": [
            {"reasonCode": code, "count": str(cnt), "percentage": _pct_of(cnt)}
            for code, cnt in hard_reason_counts.most_common(5)
        ],
    }

    policy_net = report.policy.rupees_recovered - report.policy.retry_cost_spent
    naive_net = report.naive.rupees_recovered - report.naive.retry_cost_spent
    backtest_data = {
        "policyRecoveredRevenue": _inr(report.policy.rupees_recovered),
        "policyRetries": str(report.policy.attempts),
        "naiveRetryRecoveredRevenue": _inr(report.naive.rupees_recovered),
        "naiveRetries": str(report.naive.attempts),
        "improvement": _inr(policy_net - naive_net),
        "improvementPercentage": f"{((policy_net - naive_net) / naive_net * 100.0) if naive_net else 0:+.0f}%",
        "retriesAvoided": str(report.naive.attempts - report.policy.attempts),
        "retriesAvoidedPercentage": _pct(report.useless_retries_avoided_pct),
        "seed": seed,
        "runId": f"BT_run_{run.id}",
        "baselineDescription": "Baseline: Naive retry everything on same data set",
    }

    return {
        "merchantContext": merchant_context,
        "kpiMetrics": kpi_metrics,
        "failedPaymentsData": failed_payments,
        "bucketSummaryData": bucket_summary,
        "hardDeclineReportData": hard_decline_report,
        "backtestData": backtest_data,
    }