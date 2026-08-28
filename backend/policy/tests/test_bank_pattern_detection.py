"""
test_bank_pattern_detection.py

Run:
    python3 -m pytest policy/test_bank_pattern_detection.py -v
"""

import ast
import inspect
from datetime import date, timedelta

import pytest

import bank_pattern_detection as bpd
from bank_pattern_detection import detect_systemic_days, is_bank_flagged_on, SystemicFlag


BASE_DAY = date(2026, 3, 1)


def make_event(bank: str, day: date, reason_code: str) -> dict:
    return {"bank": bank, "reason_code": reason_code, "timestamp": day.isoformat()}


class TestIsolationFromGroundTruth:
    def test_module_never_imports_simulator_ground_truth_or_gateway(self):
        source = inspect.getsource(bpd)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module is None or "ground_truth" not in (node.module or "")
                assert node.module is None or "gateway" not in (node.module or "")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "ground_truth" not in alias.name
                    assert "gateway" not in alias.name

    def test_only_transient_reason_codes_count_toward_signal(self):
        events = [make_event("HDFC", BASE_DAY, "CARD_EXPIRED")] * 20  # not transient
        flags = detect_systemic_days(events)
        assert flags == []  # no transient-reason events at all -> nothing to flag


class TestBaselineRequirement:
    def test_no_flags_before_minimum_baseline_established(self):
        # Only 3 days of history -> below default min_baseline_points=5
        events = [
            make_event("HDFC", BASE_DAY + timedelta(days=i), "NETWORK_ERROR")
            for i in range(3)
        ]
        flags = detect_systemic_days(events)
        assert flags == []

    def test_flags_appear_once_baseline_is_long_enough(self):
        events = []
        for i in range(10):
            events.append(make_event("HDFC", BASE_DAY + timedelta(days=i), "NETWORK_ERROR"))
        spike_day = BASE_DAY + timedelta(days=10)
        for _ in range(10):
            events.append(make_event("HDFC", spike_day, "BANK_TIMEOUT"))
        flags = detect_systemic_days(events)
        assert any(f.day == spike_day for f in flags)


class TestZScoreSpikeDetection:
    def test_quiet_baseline_then_clear_spike_is_flagged(self):
        events = []
        # 15 quiet days: 0-1 failures/day
        for i in range(15):
            d = BASE_DAY + timedelta(days=i)
            if i % 3 == 0:
                events.append(make_event("ICICI", d, "NETWORK_ERROR"))
        spike_day = BASE_DAY + timedelta(days=15)
        for _ in range(9):
            events.append(make_event("ICICI", spike_day, "BANK_TIMEOUT"))

        flags = detect_systemic_days(events)
        spike_flags = [f for f in flags if f.day == spike_day]
        assert len(spike_flags) == 1
        assert spike_flags[0].observed_count == 9
        assert spike_flags[0].z_score >= bpd.DEFAULT_Z_THRESHOLD

    def test_mild_daily_variation_is_not_flagged(self):
        # Steady 2-3 failures/day, no real spike -> nothing should trip
        events = []
        for i in range(20):
            d = BASE_DAY + timedelta(days=i)
            count = 2 if i % 2 == 0 else 3
            for _ in range(count):
                events.append(make_event("SBI", d, "NETWORK_ERROR"))
        flags = detect_systemic_days(events)
        assert flags == []

    def test_each_bank_judged_against_its_own_baseline(self):
        # HDFC normally noisy (5/day), Axis normally quiet (0-1/day).
        # A day with 5 failures should NOT flag HDFC but SHOULD flag Axis.
        events = []
        for i in range(15):
            d = BASE_DAY + timedelta(days=i)
            for _ in range(5):
                events.append(make_event("HDFC", d, "NETWORK_ERROR"))
            if i % 4 == 0:
                events.append(make_event("Axis", d, "NETWORK_ERROR"))

        test_day = BASE_DAY + timedelta(days=15)
        for _ in range(5):
            events.append(make_event("HDFC", test_day, "NETWORK_ERROR"))
            events.append(make_event("Axis", test_day, "NETWORK_ERROR"))

        flags = detect_systemic_days(events)
        hdfc_flags = [f for f in flags if f.bank == "HDFC" and f.day == test_day]
        axis_flags = [f for f in flags if f.bank == "Axis" and f.day == test_day]
        assert hdfc_flags == []  # 5 is HDFC's normal, not a spike for HDFC
        assert len(axis_flags) == 1  # 5 is way above Axis's normal ~0-1

    def test_zero_variance_baseline_flags_any_positive_deviation(self):
        # PNB is observed (via non-transient events) for 6 quiet days with
        # zero transient failures, establishing a real zero-variance
        # baseline, then a spike shows up.
        events = [
            make_event("PNB", BASE_DAY + timedelta(days=i), "CARD_EXPIRED")
            for i in range(6)
        ]
        spike_day = BASE_DAY + timedelta(days=6)
        events.append(make_event("PNB", spike_day, "NETWORK_ERROR"))

        flags = detect_systemic_days(events)
        assert any(f.day == spike_day and f.bank == "PNB" for f in flags)

    def test_days_before_observation_start_are_not_treated_as_quiet(self):
        # Only ONE day of real observation exists for this bank -- even
        # though target_day - 14 would land on "day -13" if we padded with
        # zeros, there's no real history there, so no flag should fire.
        events = [make_event("PNB", BASE_DAY, "NETWORK_ERROR")]
        flags = detect_systemic_days(events)
        assert flags == []


class TestThresholdAndParams:
    def test_higher_threshold_yields_fewer_or_equal_flags(self):
        events = []
        for i in range(15):
            d = BASE_DAY + timedelta(days=i)
            if i % 3 == 0:
                events.append(make_event("Kotak", d, "NETWORK_ERROR"))
        spike_day = BASE_DAY + timedelta(days=15)
        for _ in range(6):
            events.append(make_event("Kotak", spike_day, "BANK_TIMEOUT"))

        lenient = detect_systemic_days(events, z_threshold=1.0)
        strict = detect_systemic_days(events, z_threshold=10.0)
        assert len(strict) <= len(lenient)


class TestLookupHelper:
    def test_is_bank_flagged_on_true_and_false_cases(self):
        flags = [
            SystemicFlag(
                bank="HDFC", day=BASE_DAY, observed_count=9, baseline_mean=1.0,
                baseline_stdev=0.5, z_score=16.0, notes="test",
            )
        ]
        assert is_bank_flagged_on(flags, "HDFC", BASE_DAY) is True
        assert is_bank_flagged_on(flags, "HDFC", BASE_DAY + timedelta(days=1)) is False
        assert is_bank_flagged_on(flags, "ICICI", BASE_DAY) is False


class TestMultiBankIndependence:
    def test_flags_carry_correct_bank_label(self):
        events = []
        for i in range(10):
            d = BASE_DAY + timedelta(days=i)
            if i % 4 == 0:
                events.append(make_event("Yes Bank", d, "NETWORK_ERROR"))
        spike_day = BASE_DAY + timedelta(days=10)
        for _ in range(7):
            events.append(make_event("Yes Bank", spike_day, "BANK_TIMEOUT"))

        flags = detect_systemic_days(events)
        assert all(f.bank == "Yes Bank" for f in flags)