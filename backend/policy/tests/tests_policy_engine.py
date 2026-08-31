"""
test_policy_engine.py

Tests for policy_engine.py — the Stage-3 orchestrator wiring
ev_gate -> retry_timing -> bank_pattern_detection.

These tests use a lightweight stand-in for classification.classifier's
ClassificationResult (same field names) so this file has no import
dependency on the classification/ package — policy_engine only ever
reads attributes off whatever object it's given, so a stand-in with the
right shape is a faithful test double.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pytest

from policy.bank_pattern_detection import SystemicFlag
from policy.ev_gate import Bucket
from policy.policy_engine import decide_batch, decide_event, summarize


@dataclass
class FakeClassification:
    customer_id: str
    timestamp: str
    amount: float
    reason_code_raw: str
    bucket: str
    confidence: float = 1.0


def flag(bank: str, day: date) -> SystemicFlag:
    return SystemicFlag(
        bank=bank, day=day, observed_count=8, baseline_mean=1.0, baseline_stdev=0.5, z_score=14.0, notes="test flag"
    )


# ---------------------------------------------------------------- HARD ----

def test_hard_decline_never_retried_regardless_of_amount():
    c = FakeClassification("cust_1", "2026-03-10", 999_999, "CARD_EXPIRED", "HARD")
    d = decide_event(c, bank="HDFC")

    assert d.ev_decision.forced_no_retry is True
    assert d.ev_decision.should_retry is False
    assert d.final_retry_date is None
    assert d.timing_decision is None
    assert d.bank_adjusted is False


def test_hard_decline_ignores_systemic_flags_entirely():
    c = FakeClassification("cust_1", "2026-03-10", 500, "MANDATE_REVOKED", "HARD")
    flags = [flag("HDFC", date(2026, 3, 10))]
    d = decide_event(c, bank="HDFC", systemic_flags=flags)

    assert d.final_retry_date is None
    assert d.bank_adjusted is False


# ---------------------------------------------------------------- SOFT ----

def test_soft_decline_ev_positive_gets_a_retry_date():
    c = FakeClassification("cust_2", "2026-03-10", 499, "INSUFFICIENT_FUNDS", "SOFT")
    d = decide_event(c, bank="HDFC")

    assert d.ev_decision.should_retry is True
    assert d.timing_decision is not None
    assert d.final_retry_date == date(2026, 3, 13)  # reason-default 3-day window


def test_soft_decline_ev_negative_amount_too_small_skips_retry():
    # retry_cost (2.0) > p_recover * amount for a tiny amount -> EV <= 0
    c = FakeClassification("cust_3", "2026-03-10", 1, "INSUFFICIENT_FUNDS", "SOFT")
    d = decide_event(c, bank="HDFC")

    assert d.ev_decision.should_retry is False
    assert d.ev_decision.forced_no_retry is False  # this is an EV call, not the HARD rule
    assert d.final_retry_date is None
    assert d.timing_decision is None


def test_customer_history_overrides_reason_default_window():
    c = FakeClassification("cust_4", "2026-03-10", 499, "INSUFFICIENT_FUNDS", "SOFT")
    d = decide_event(c, bank="HDFC", customer_retry_success_history_days=[5, 4, 6])

    assert d.timing_decision.source == "customer_history"
    assert d.final_retry_date == date(2026, 3, 15)  # median offset 5, no bank flag


# ---------------------------------------------------- bank pattern push ----

def test_bank_flagged_on_suggested_date_pushes_one_day_forward():
    c = FakeClassification("cust_5", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    # reason default delay is 1 day -> suggested date lands on 2026-03-11
    flags = [flag("ICICI", date(2026, 3, 11))]
    d = decide_event(c, bank="ICICI", systemic_flags=flags)

    assert d.bank_adjusted is True
    assert d.bank_adjustment_days == 1
    assert d.final_retry_date == date(2026, 3, 12)
    assert any("systemically degraded" in line for line in d.audit_trail)


def test_bank_flagged_across_consecutive_days_pushes_past_all_of_them():
    c = FakeClassification("cust_6", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    flags = [
        flag("ICICI", date(2026, 3, 11)),
        flag("ICICI", date(2026, 3, 12)),
        flag("ICICI", date(2026, 3, 13)),
    ]
    d = decide_event(c, bank="ICICI", systemic_flags=flags)

    assert d.bank_adjustment_days == 3
    assert d.final_retry_date == date(2026, 3, 14)  # first unflagged day


def test_bank_not_flagged_on_suggested_date_no_adjustment():
    c = FakeClassification("cust_7", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    flags = [flag("ICICI", date(2026, 3, 20))]  # unrelated day
    d = decide_event(c, bank="ICICI", systemic_flags=flags)

    assert d.bank_adjusted is False
    assert d.bank_adjustment_days == 0
    assert d.final_retry_date == date(2026, 3, 11)


def test_bank_push_respects_max_cap():
    from policy.policy_engine import MAX_BANK_PUSH_DAYS

    c = FakeClassification("cust_8", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    flags = [flag("ICICI", date(2026, 3, 11) + __import__("datetime").timedelta(days=i)) for i in range(50)]
    d = decide_event(c, bank="ICICI", systemic_flags=flags)

    assert d.bank_adjustment_days == MAX_BANK_PUSH_DAYS
    assert "cap" in d.audit_trail[-1]


def test_only_the_flagged_banks_customers_are_affected():
    c_icici = FakeClassification("cust_9", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    c_hdfc = FakeClassification("cust_10", "2026-03-10", 1499, "BANK_TIMEOUT", "SOFT")
    flags = [flag("ICICI", date(2026, 3, 11))]

    d_icici = decide_event(c_icici, bank="ICICI", systemic_flags=flags)
    d_hdfc = decide_event(c_hdfc, bank="HDFC", systemic_flags=flags)

    assert d_icici.bank_adjusted is True
    assert d_hdfc.bank_adjusted is False
    assert d_hdfc.final_retry_date == date(2026, 3, 11)


# --------------------------------------------------------------- UNCERTAIN --

def test_uncertain_high_confidence_can_still_get_a_retry():
    c = FakeClassification("cust_11", "2026-03-10", 5000, "UNKNOWN_DECLINE", "UNCERTAIN", confidence=0.9)
    d = decide_event(c, bank="HDFC")

    assert d.ev_decision.should_retry is True  # 0.30 * 0.9 * 5000 - 2 > 0
    assert d.final_retry_date is not None


def test_uncertain_low_confidence_ev_too_small_skips():
    c = FakeClassification("cust_12", "2026-03-10", 15, "UNKNOWN_DECLINE", "UNCERTAIN", confidence=0.3)
    d = decide_event(c, bank="HDFC")

    assert d.ev_decision.should_retry is False
    assert d.final_retry_date is None


# ------------------------------------------------------------------ batch --

def test_decide_batch_pulls_bank_from_event_not_classification():
    classifications = [
        FakeClassification("cust_13", "2026-03-10", 499, "INSUFFICIENT_FUNDS", "SOFT"),
        FakeClassification("cust_14", "2026-03-10", 999, "CARD_EXPIRED", "HARD"),
    ]
    events = [{"bank": "HDFC"}, {"bank": "ICICI"}]

    results = decide_batch(events, classifications)

    assert results[0].bank == "HDFC"
    assert results[1].bank == "ICICI"


def test_decide_batch_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        decide_batch(events=[{"bank": "HDFC"}], classifications=[])


def test_decide_batch_applies_per_customer_history_map():
    classifications = [FakeClassification("cust_15", "2026-03-10", 499, "INSUFFICIENT_FUNDS", "SOFT")]
    events = [{"bank": "HDFC"}]
    history = {"cust_15": [5, 4, 6]}

    results = decide_batch(events, classifications, customer_retry_success_history_days=history)

    assert results[0].timing_decision.source == "customer_history"
    assert results[0].final_retry_date == date(2026, 3, 15)


def test_summarize_counts_buckets_correctly():
    classifications = [
        FakeClassification("cust_16", "2026-03-10", 999, "CARD_EXPIRED", "HARD"),
        FakeClassification("cust_17", "2026-03-10", 1, "INSUFFICIENT_FUNDS", "SOFT"),
        FakeClassification("cust_18", "2026-03-10", 499, "INSUFFICIENT_FUNDS", "SOFT"),
    ]
    events = [{"bank": "HDFC"}] * 3

    results = decide_batch(events, classifications)
    summary = summarize(results)

    assert summary["total"] == 3
    assert summary["no_retry_hard"] == 1
    assert summary["no_retry_ev_negative"] == 1
    assert summary["retried"] == 1


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))