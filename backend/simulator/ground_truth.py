"""
ground_truth.py

The HIDDEN state of a synthetic customer. Nothing in this file is ever
returned directly to the classifier / policy engine — it exists only so
the simulator can resolve "would this payment actually have succeeded?"
and so the backtest can later grade the policy against the real answer.

Think of it as the answer key a teacher holds, not something the student
(the policy engine) is allowed to read.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class CustomerGroundTruth:
    customer_id: str
    bank: str

    # --- Recurring payment being tracked ---
    subscription_amount: float
    due_day: int  # day-of-month the subscription attempts (1-28)

    # --- Balance simulation (soft-decline resolution) ---
    starting_balance: float
    salary_day: int  # day-of-month salary/credit lands (1-28)
    salary_amount: float
    daily_burn: float  # average balance drawdown per day between credits

    # --- Hard-decline instrument state ---
    card_valid_until: date | None  # None => not a card mandate (e.g. UPI)
    mandate_revoked_on: date | None  # None => never revoked
    account_closed_on: date | None  # None => never closed

    # --- Transient/systemic noise ---
    base_network_error_rate: float = 0.03  # small chance of a one-off blip
    merchant_id: str = "MERCH_001"

    def balance_on(self, on_date: date) -> float:
        """
        Reconstructs the account balance on a given date using a simple
        sawtooth model: balance jumps up by `salary_amount` on each
        `salary_day`, and decays by `daily_burn` every day in between.
        This is intentionally simple — it's a stand-in for real bank-ledger
        data the aggregator would never actually have access to.
        """
        # Walk backwards to the most recent salary credit on/before on_date.
        if on_date.day >= self.salary_day:
            last_credit = date(on_date.year, on_date.month, self.salary_day)
        else:
            prev_month = on_date.month - 1 or 12
            prev_year = on_date.year if on_date.month > 1 else on_date.year - 1
            last_credit = date(prev_year, prev_month, self.salary_day)

        days_since_credit = (on_date - last_credit).days
        balance = self.starting_balance + self.salary_amount - (days_since_credit * self.daily_burn)
        return max(balance, 0.0)

    def is_card_expired(self, on_date: date) -> bool:
        return self.card_valid_until is not None and on_date > self.card_valid_until

    def is_mandate_revoked(self, on_date: date) -> bool:
        return self.mandate_revoked_on is not None and on_date >= self.mandate_revoked_on

    def is_account_closed(self, on_date: date) -> bool:
        return self.account_closed_on is not None and on_date >= self.account_closed_on


BANKS = ["HDFC", "ICICI", "SBI", "Axis", "Kotak", "PNB", "Yes Bank"]

# Synthetic merchants — customers are round-robin assigned across these,
# so "select a merchant" filters the same underlying dataset instead of
# needing a separate generation run per merchant.
MERCHANTS = [
    {"id": "MERCH_001", "name": "StreamFlix India", "industry": "Streaming", "plan": "Premium"},
    {"id": "MERCH_002", "name": "FitPro Subscriptions", "industry": "Fitness", "plan": "Growth"},
    {"id": "MERCH_003", "name": "CloudNote SaaS", "industry": "SaaS", "plan": "Enterprise"},
    {"id": "MERCH_004", "name": "DailyNews+", "industry": "Media", "plan": "Starter"},
    {"id": "MERCH_005", "name": "EduLearn Academy", "industry": "EdTech", "plan": "Growth"},
]


def _pick_hard_decline_flags(rng: random.Random, signup: date, horizon_days: int) -> dict:
    """
    Decide, once at generation time, whether this customer's instrument
    will fail permanently at some point in the simulation horizon.
    Roughly: ~6% card-expiry, ~3% mandate-revoke, ~1.5% account-closure —
    tuned to be rare, since these are the exception not the rule.
    """
    flags = {"card_valid_until": None, "mandate_revoked_on": None, "account_closed_on": None}
    roll = rng.random()
    if roll < 0.06:
        expiry_offset = rng.randint(10, horizon_days - 5)
        flags["card_valid_until"] = signup + timedelta(days=expiry_offset)
    elif roll < 0.09:
        revoke_offset = rng.randint(10, horizon_days - 5)
        flags["mandate_revoked_on"] = signup + timedelta(days=revoke_offset)
    elif roll < 0.105:
        close_offset = rng.randint(10, horizon_days - 5)
        flags["account_closed_on"] = signup + timedelta(days=close_offset)
    return flags


def generate_customers(n: int, seed: int, start_date: date, horizon_days: int) -> list[CustomerGroundTruth]:
    """
    Generates `n` synthetic customers with a hidden financial ground truth.
    Deterministic for a given seed — same seed always produces the same
    population, which is what makes the backtest re-runnable and provable.
    """
    rng = random.Random(seed)
    customers = []

    for i in range(n):
        subscription_amount = rng.choice([199, 299, 499, 999, 1499])
        due_day = rng.randint(1, 28)
        salary_day = rng.randint(1, 28)
        salary_amount = rng.uniform(15000, 90000)
        starting_balance = rng.uniform(500, 5000)
        daily_burn = salary_amount / rng.uniform(20, 35)  # spends most of it over the month

        flags = _pick_hard_decline_flags(rng, start_date, horizon_days)

        customers.append(
            CustomerGroundTruth(
                customer_id=f"cust_{i:05d}",
                bank=rng.choice(BANKS),
                merchant_id=MERCHANTS[i % len(MERCHANTS)]["id"],
                subscription_amount=subscription_amount,
                due_day=due_day,
                starting_balance=starting_balance,
                salary_day=salary_day,
                salary_amount=salary_amount,
                daily_burn=daily_burn,
                base_network_error_rate=rng.uniform(0.01, 0.05),
                **flags,
            )
        )

    return customers