"""
test_retry_timing.py

Run:
    python3 -m pytest policy/test_retry_timing.py -v
"""

from datetime import date

import pytest

from ev_gate import Bucket
from retry_timing import suggest_retry_date, REASON_DEFAULT_RETRY_DELAY_DAYS


TODAY = date(2026, 3, 15)


class TestHardBucketGuard:
    def test_hard_bucket_raises(self):
        with pytest.raises(ValueError):
            suggest_retry_date("CARD_EXPIRED", Bucket.HARD, TODAY)


class TestReasonDefaults:
    def test_network_error_default_is_zero_days(self):
        d = suggest_retry_date("NETWORK_ERROR", Bucket.SOFT, TODAY)
        assert d.delay_days == 0
        assert d.suggested_retry_date == TODAY
        assert d.source == "reason_default"

    def test_insufficient_funds_default_is_three_days(self):
        d = suggest_retry_date("INSUFFICIENT_FUNDS", Bucket.SOFT, TODAY)
        assert d.delay_days == 3
        assert d.source == "reason_default"

    def test_unknown_soft_reason_falls_back_to_bucket(self):
        d = suggest_retry_date("SOME_NEW_SOFT_CODE", Bucket.SOFT, TODAY)
        assert d.source == "bucket_fallback"
        assert d.delay_days == 2


class TestCustomerHistoryTakesPriority:
    def test_history_overrides_reason_default(self):
        # Reason default for INSUFFICIENT_FUNDS is 3, but this customer's
        # own history says 5 -- history should win.
        d = suggest_retry_date(
            "INSUFFICIENT_FUNDS", Bucket.SOFT, TODAY, customer_retry_success_history_days=[5, 5, 5]
        )
        assert d.source == "customer_history"
        assert d.delay_days == 5

    def test_uses_median_not_mean_to_resist_outliers(self):
        # median([2, 3, 100]) = 3, mean would be ~35 -- median is the
        # defensible choice against a one-off outlier.
        d = suggest_retry_date(
            "INSUFFICIENT_FUNDS", Bucket.SOFT, TODAY, customer_retry_success_history_days=[2, 3, 100]
        )
        assert d.delay_days == 3

    def test_only_recent_history_points_used(self):
        # 10 old points at delay=1, then 3 recent points at delay=9 -- with
        # MAX_HISTORY_POINTS_USED=10 and 13 total points, only the most
        # recent 10 are considered (mix of old 1s and new 9s).
        history = [1] * 10 + [9] * 3
        d = suggest_retry_date("INSUFFICIENT_FUNDS", Bucket.SOFT, TODAY, customer_retry_success_history_days=history)
        # last 10 points = [1]*7 + [9]*3 -> median = 1
        assert d.delay_days == 1

    def test_empty_history_list_falls_back_to_default(self):
        d = suggest_retry_date("BANK_TIMEOUT", Bucket.SOFT, TODAY, customer_retry_success_history_days=[])
        assert d.source == "reason_default"
        assert d.delay_days == REASON_DEFAULT_RETRY_DELAY_DAYS["BANK_TIMEOUT"]


class TestUncertainBucket:
    def test_uncertain_with_no_history_uses_bucket_fallback(self):
        d = suggest_retry_date("UNKNOWN_DECLINE", Bucket.UNCERTAIN, TODAY)
        assert d.source == "bucket_fallback"
        assert d.delay_days == 2

    def test_uncertain_with_history_still_prefers_history(self):
        d = suggest_retry_date(
            "UNKNOWN_DECLINE", Bucket.UNCERTAIN, TODAY, customer_retry_success_history_days=[7]
        )
        assert d.source == "customer_history"
        assert d.delay_days == 7


class TestDateArithmetic:
    def test_suggested_date_is_failure_date_plus_delay(self):
        d = suggest_retry_date("INSUFFICIENT_FUNDS", Bucket.SOFT, TODAY)
        assert (d.suggested_retry_date - TODAY).days == d.delay_days