"""
generator.py

The orchestrator: builds a synthetic customer population, scripts one or
two systemic bank-degradation windows, then walks the calendar to produce
the OBSERVABLE event stream — the only thing downstream layers
(classification, policy, backtest) are allowed to see.

Two outputs are produced, deliberately kept apart:
  - `events`      -> observable failure events (reason_code, date, amount)
  - `ground_truth`-> hidden customer state, kept for backtest grading only

Run this file directly for a quick sanity demo:
    python -m simulator.generator
"""

from __future__ import annotations

import random
from dataclasses import asdict
from datetime import date, timedelta

from .gateway import BankDegradationWindow, MockGateway, PaymentOutcome
from .ground_truth import BANKS, generate_customers


class SyntheticDataset:
    def __init__(self, seed: int, n_customers: int = 200, months: int = 4):
        self.seed = seed
        self.start_date = date(2026, 1, 1)
        self.horizon_days = months * 31

        self.customers = generate_customers(
            n=n_customers, seed=seed, start_date=self.start_date, horizon_days=self.horizon_days
        )
        self.degradation_windows = self._script_degradation(seed)
        self.gateway = MockGateway(seed=seed, degradation_windows=self.degradation_windows)

        self.events: list[PaymentOutcome] = []
        self._run()

    def _script_degradation(self, seed: int) -> list[BankDegradationWindow]:
        """
        Injects one deliberate 'a specific bank is having a bad week' event
        so the cross-customer pattern-detection logic has something real
        to find later. Deterministic per seed.
        """
        rng = random.Random(seed + 1)
        bank = rng.choice(BANKS)
        offset = rng.randint(20, self.horizon_days - 15)
        start = self.start_date + timedelta(days=offset)
        end = start + timedelta(days=rng.randint(3, 7))
        return [BankDegradationWindow(bank=bank, start=start, end=end, extra_timeout_rate=0.55)]

    def _run(self) -> None:
        """Walks each month's due date for every customer and records failures."""
        for customer in self.customers:
            for month_offset in range(self.horizon_days // 30):
                year = self.start_date.year + (self.start_date.month - 1 + month_offset) // 12
                month = (self.start_date.month - 1 + month_offset) % 12 + 1
                try:
                    due_date = date(year, month, customer.due_day)
                except ValueError:
                    continue  # e.g. day 30/31 in Feb, just skip that cycle
                outcome = self.gateway.attempt_payment(customer, due_date)
                if not outcome.success:
                    outcome.bank = outcome.bank or customer.bank
                    outcome.merchant_id = outcome.merchant_id or customer.merchant_id
                    self.events.append(outcome)

    def observable_events_as_dicts(self) -> list[dict]:
        """
        This is the ONLY view of the data the classification/policy layers
        should ever consume — no ground-truth fields present. `raw_text` is
        included because a real gateway would surface it too when the
        reason code itself is UNKNOWN_DECLINE; `true_reason_code` is
        deliberately withheld here even though it lives on the event.
        """
        return [
            {
                "customer_id": e.customer_id,
                "timestamp": e.timestamp.isoformat(),
                "amount": e.amount,
                "reason_code": e.reason_code.value,
                "raw_text": e.raw_text,
                "bank": e.bank,
                "merchant_id": e.merchant_id,
            }
            for e in self.events
        ]

    def event_true_labels(self) -> dict:
        """Backtest-only: {(customer_id, timestamp) -> true_reason_code}."""
        return {(e.customer_id, e.timestamp.isoformat()): e.true_reason_code.value for e in self.events}

    def ground_truth_lookup(self) -> dict:
        """Backtest-only: hidden state keyed by customer_id, for grading."""
        return {c.customer_id: asdict(c) for c in self.customers}


if __name__ == "__main__":
    ds = SyntheticDataset(seed=42, n_customers=200, months=4)
    events = ds.observable_events_as_dicts()

    print(f"Generated {len(ds.customers)} customers, {len(events)} failure events, seed=42\n")
    print("Sample observable events (this is ALL the classifier ever sees):")
    for e in events[:5]:
        print(" ", e)

    from collections import Counter
    reason_counts = Counter(e["reason_code"] for e in events)
    print("\nReason code distribution:")
    for code, count in reason_counts.most_common():
        print(f"  {code:20s} {count}")

    print(f"\nInjected degradation window: {ds.degradation_windows[0]}")

    # Determinism check
    ds2 = SyntheticDataset(seed=42, n_customers=200, months=4)
    same = ds.observable_events_as_dicts() == ds2.observable_events_as_dicts()
    print(f"\nReproducibility check (same seed -> same events): {same}")

    