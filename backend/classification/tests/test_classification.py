"""
tests/test_classification.py

Covers:
  - every known ReasonCode lands in the bucket reason_codes.py says it
    should (rule-table correctness), at full confidence
  - unknown/free-text reason codes are routed to the LLM fallback path
  - low-confidence outcomes are always forced to UNCERTAIN + flagged for
    human review, regardless of what bucket the fallback guessed
  - classify_batch on the real generator output never crashes and
    produces one result per event
  - the classifier module never touches ground truth (isolation, same
    spirit as test_simulator.py's ground-truth isolation test)
"""

import pytest

from classification.classifier import CONFIDENCE_THRESHOLD, classify_batch, classify_event, summarize
from simulator.generator import SyntheticDataset
from simulator.reason_codes import HARD_CODES, SOFT_CODES, ReasonCode


def make_event(reason_code: str, **overrides) -> dict:
    base = {"customer_id": "cust_00001", "timestamp": "2026-02-01", "amount": 499, "reason_code": reason_code}
    base.update(overrides)
    return base


@pytest.mark.parametrize("code", list(HARD_CODES))
def test_hard_codes_classified_hard_at_full_confidence(code):
    result = classify_event(make_event(code.value))
    assert result.bucket == "HARD"
    assert result.confidence == 1.0
    assert result.source == "rule"
    assert not result.flagged_for_human_review


@pytest.mark.parametrize("code", list(SOFT_CODES))
def test_soft_codes_classified_soft_at_full_confidence(code):
    result = classify_event(make_event(code.value))
    assert result.bucket == "SOFT"
    assert result.confidence == 1.0
    assert result.source == "rule"
    assert not result.flagged_for_human_review


def test_known_uncertain_code_routes_to_uncertain_via_rule():
    result = classify_event(make_event(ReasonCode.UNKNOWN_DECLINE.value))
    assert result.bucket == "UNCERTAIN"
    assert result.source == "rule"  # UNKNOWN_DECLINE is itself a recognised enum member


def test_unrecognised_free_text_routes_to_llm_fallback():
    result = classify_event(make_event("Card was reported blocked by issuer"))
    assert result.source == "llm_fallback"
    assert result.bucket in {"HARD", "SOFT", "UNCERTAIN"}


def test_low_confidence_llm_result_forced_uncertain_and_flagged():
    # Empty text -> llm_fallback.classify_via_llm returns confidence 0.0,
    # which must never survive as a non-UNCERTAIN, non-flagged result.
    result = classify_event(make_event(""))
    assert result.bucket == "UNCERTAIN"
    assert result.flagged_for_human_review
    assert result.confidence < CONFIDENCE_THRESHOLD


def test_missing_reason_code_key_raises():
    with pytest.raises(KeyError):
        classify_event({"customer_id": "cust_00001", "timestamp": "2026-02-01", "amount": 499})


def test_classify_batch_on_real_generator_output_covers_every_event():
    ds = SyntheticDataset(seed=42, n_customers=200, months=4)
    events = ds.observable_events_as_dicts()
    results = classify_batch(events)
    assert len(results) == len(events)
    # Every event in this dataset has a recognised structured reason_code,
    # so the rule path should handle all of them -- zero LLM fallback calls.
    summary = summarize(results)
    assert summary["by_source"].get("llm_fallback", 0) == 0
    assert summary["total"] == len(events)


def test_classification_module_never_imports_ground_truth():
    """
    Isolation guard: the classifier must only ever see the observable
    event shape, never simulator.ground_truth or simulator.gateway. This
    checks the actual import graph, not just intent in a docstring.
    """
    import ast
    import inspect

    from classification import classifier as classifier_module

    source = inspect.getsource(classifier_module)
    tree = ast.parse(source)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name)

    assert "simulator.ground_truth" not in imported_modules
    assert "simulator.gateway" not in imported_modules