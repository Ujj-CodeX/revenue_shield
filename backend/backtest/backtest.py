
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from policy.bank_pattern_detection import detect_systemic_days
from classification.classifier import classify_batch
from policy.ev_gate import DEFAULT_RETRY_COST
from policy.policy_engine import decide_batch
from simulator.gateway import BankDegradationWindow, MockGateway
from simulator.generator import SyntheticDataset
from simulator.ground_truth import CustomerGroundTruth

NAIVE_RETRY_DELAY_DAYS = 1  # the naive baseline's one-size-fits-all retry delay


@dataclass
class ArmResult:
    name: str  # "policy" | "naive"
    attempts: int
    successes: int
    failures: int
    rupees_recovered: float
    retry_cost_spent: float

    @property
    def useless_retries(self) -> int:
        return self.failures

    @property
    def success_rate(self) -> float:
        return self.successes / self.attempts if self.attempts else 0.0


@dataclass
class BacktestReport:
    seed: int
    total_failures: int
    hard_declines_skipped: int  # never eligible for retry in either arm's fair comparison
    policy: ArmResult
    naive: ArmResult
    useless_retries_avoided_pct: float  # policy vs naive, as a % of naive's useless retries
    notes: list[str] = field(default_factory=list)


def _run_arm(
    name: str,
    retries: list[tuple[CustomerGroundTruth, date]],
    seed: int,
    degradation_windows: list[BankDegradationWindow],
    retry_cost: float,
) -> ArmResult:
    
    gateway = MockGateway(seed=seed, degradation_windows=degradation_windows)
    successes = 0
    rupees_recovered = 0.0

    for customer, retry_date in retries:
        outcome = gateway.attempt_payment(customer, retry_date)
        if outcome.success:
            successes += 1
            rupees_recovered += customer.subscription_amount

    attempts = len(retries)
    return ArmResult(
        name=name,
        attempts=attempts,
        successes=successes,
        failures=attempts - successes,
        rupees_recovered=rupees_recovered,
        retry_cost_spent=attempts * retry_cost,
    )


def run_backtest(
    seed: int = 42,
    n_customers: int = 200,
    months: int = 4,
    retry_cost: float = DEFAULT_RETRY_COST,
    merchant_id: str | None = None,
) -> BacktestReport:
    
   
    
    ds = SyntheticDataset(seed=seed, n_customers=n_customers, months=months)
    events = ds.observable_events_as_dicts()
    if merchant_id:
        events = [e for e in events if e.get("merchant_id") == merchant_id]
    customers_by_id = {c.customer_id: c for c in ds.customers}

    classifications = classify_batch(events)
    systemic_flags = detect_systemic_days(events)
    decisions = decide_batch(events, classifications, systemic_flags=systemic_flags, retry_cost=retry_cost)

    hard_skipped = sum(1 for d in decisions if d.ev_decision.forced_no_retry)

    policy_retries = [
        (customers_by_id[d.customer_id], d.final_retry_date) for d in decisions if d.final_retry_date is not None
    ]
    naive_retries = [
        (customers_by_id[e["customer_id"]], date.fromisoformat(e["timestamp"]) + timedelta(days=NAIVE_RETRY_DELAY_DAYS))
        for e in events
    ]

    policy_arm = _run_arm("policy", policy_retries, seed, ds.degradation_windows, retry_cost)
    naive_arm = _run_arm("naive", naive_retries, seed, ds.degradation_windows, retry_cost)

    if naive_arm.useless_retries > 0:
        avoided_pct = 100.0 * (naive_arm.useless_retries - policy_arm.useless_retries) / naive_arm.useless_retries
    else:
        avoided_pct = 0.0

    notes = [
        f"{len(events)} total observable failures; {hard_skipped} were HARD declines (never retried by policy).",
        f"Naive retries every failure {NAIVE_RETRY_DELAY_DAYS} day(s) later, including HARD declines the policy correctly skips.",
        f"Policy retried {policy_arm.attempts}/{len(events)} failures; naive retried {naive_arm.attempts}/{len(events)}.",
    ]

    return BacktestReport(
        seed=seed,
        total_failures=len(events),
        hard_declines_skipped=hard_skipped,
        policy=policy_arm,
        naive=naive_arm,
        useless_retries_avoided_pct=avoided_pct,
        notes=notes,
    )


def print_report(report: BacktestReport) -> None:
    print(f"Backtest report (seed={report.seed}, {report.total_failures} total failures)\n")
    for name, arm in (("POLICY", report.policy), ("NAIVE", report.naive)):
        print(f"  {name:8s} attempts={arm.attempts:4d}  successes={arm.successes:4d}  "
              f"useless_retries={arm.useless_retries:4d}  success_rate={arm.success_rate:.1%}  "
              f"recovered=₹{arm.rupees_recovered:,.2f}  retry_cost=₹{arm.retry_cost_spent:,.2f}  "
              f"net=₹{arm.rupees_recovered - arm.retry_cost_spent:,.2f}")
    print(f"\n  Useless retries avoided (policy vs naive): {report.useless_retries_avoided_pct:.1f}%")
    print("\nNotes:")
    for n in report.notes:
        print(f"  - {n}")


def persist_backtest_run(report: "BacktestReport", n_customers: int = 200, months: int = 4):
    
    from .models import BacktestRun

    run = BacktestRun.objects.create(
        seed=report.seed,
        n_customers=n_customers,
        months=months,
        total_failures=report.total_failures,
        hard_declines_skipped=report.hard_declines_skipped,
        policy_attempts=report.policy.attempts,
        policy_successes=report.policy.successes,
        policy_rupees_recovered=report.policy.rupees_recovered,
        policy_retry_cost_spent=report.policy.retry_cost_spent,
        naive_attempts=report.naive.attempts,
        naive_successes=report.naive.successes,
        naive_rupees_recovered=report.naive.rupees_recovered,
        naive_retry_cost_spent=report.naive.retry_cost_spent,
        useless_retries_avoided_pct=report.useless_retries_avoided_pct,
        notes=report.notes,
    )

    from audit.logger import log_backtest_run
    log_backtest_run(report)

    return run


if __name__ == "__main__":
    report = run_backtest(seed=42, n_customers=200, months=4)
    print_report(report)

    print("\nReproducibility check (same seed -> same report):")
    report2 = run_backtest(seed=42, n_customers=200, months=4)
    same = (report.policy.rupees_recovered == report2.policy.rupees_recovered
            and report.naive.rupees_recovered == report2.naive.rupees_recovered)
    print(f"  {same}")