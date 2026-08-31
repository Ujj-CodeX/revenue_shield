"""
Tests for the ground-truth generator + mock gateway. These lock down the
three properties the whole project depends on:

1. Reproducibility  -> same seed always gives the same events (backtest proof)
2. Ground-truth isolation -> observable events never leak hidden fields
3. Decline priority -> a dead instrument always wins over a balance check
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from simulator.generator import SyntheticDataset
from simulator.gateway import MockGateway
from simulator.ground_truth import CustomerGroundTruth
from simulator.reason_codes import ReasonCode


def test_same_seed_is_fully_reproducible():
    ds1 = SyntheticDataset(seed=7, n_customers=50, months=3)
    ds2 = SyntheticDataset(seed=7, n_customers=50, months=3)
    assert ds1.observable_events_as_dicts() == ds2.observable_events_as_dicts()


def test_different_seed_changes_output():
    ds1 = SyntheticDataset(seed=1, n_customers=50, months=3)
    ds2 = SyntheticDataset(seed=2, n_customers=50, months=3)
    assert ds1.observable_events_as_dicts() != ds2.observable_events_as_dicts()


def test_observable_events_never_leak_ground_truth_fields():
    ds = SyntheticDataset(seed=42, n_customers=30, months=2)
    forbidden_keys = {
        "salary_day", "salary_amount", "starting_balance", "daily_burn",
        "card_valid_until", "mandate_revoked_on", "account_closed_on",
    }
    for event in ds.observable_events_as_dicts():
        assert forbidden_keys.isdisjoint(event.keys())
        assert set(event.keys()) == {"customer_id", "timestamp", "amount", "reason_code", "raw_text", "bank"}


def test_expired_card_always_hard_declines_even_with_healthy_balance():
    customer = CustomerGroundTruth(
        customer_id="cust_test", bank="HDFC", subscription_amount=299, due_day=10,
        starting_balance=100000, salary_day=1, salary_amount=50000, daily_burn=10,
        card_valid_until=date(2026, 1, 1), mandate_revoked_on=None, account_closed_on=None,
        base_network_error_rate=0.0,
    )
    gateway = MockGateway(seed=1)
    outcome = gateway.attempt_payment(customer, date(2026, 6, 1))
    assert outcome.success is False
    assert outcome.reason_code == ReasonCode.CARD_EXPIRED


def test_healthy_customer_with_no_flags_and_zero_noise_always_succeeds():
    customer = CustomerGroundTruth(
        customer_id="cust_healthy", bank="ICICI", subscription_amount=199, due_day=5,
        starting_balance=50000, salary_day=1, salary_amount=50000, daily_burn=1,
        card_valid_until=None, mandate_revoked_on=None, account_closed_on=None,
        base_network_error_rate=0.0,
    )
    gateway = MockGateway(seed=1)
    outcome = gateway.attempt_payment(customer, date(2026, 1, 5))
    assert outcome.success is True
    assert outcome.reason_code is None


def test_low_balance_customer_gets_insufficient_funds():
    customer = CustomerGroundTruth(
        customer_id="cust_poor", bank="SBI", subscription_amount=999, due_day=25,
        starting_balance=50, salary_day=1, salary_amount=100, daily_burn=5,
        card_valid_until=None, mandate_revoked_on=None, account_closed_on=None,
        base_network_error_rate=0.0,
    )
    gateway = MockGateway(seed=1)
    outcome = gateway.attempt_payment(customer, date(2026, 1, 25))
    assert outcome.success is False
    assert outcome.reason_code == ReasonCode.INSUFFICIENT_FUNDS