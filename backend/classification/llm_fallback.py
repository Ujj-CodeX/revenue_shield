"""
llm_fallback.py

Fallback classifier for events whose reason_code is NOT a recognised
ReasonCode enum member — i.e. missing, malformed, or free-text, exactly
the minority case described in problem statement 6.2. The rule table in
reason_lookup.py should handle everything else; this path should be rare.

Per 6.2, this is deliberately a SINGLE LLM (not a multi-model ensemble),
and the same model will later power the operator-facing Copilot Q&A.

STATUS: stubbed with a keyword heuristic so the rest of the pipeline
(confidence thresholding, human-review routing, tests) can be built and
exercised without wiring an API key yet. `classify_via_llm()` is the only
function that needs to change when we swap in a real call — its
signature and return type are the real contract.

Swap-in point for later:
    from anthropic import Anthropic
    client = Anthropic()
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": PROMPT.format(text=raw_reason_text)}],
    )
    # parse response into LLMClassification
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMClassification:
    bucket: str  # "HARD" | "SOFT" | "UNCERTAIN"
    confidence: float  # 0.0-1.0, heuristic's self-reported confidence
    reasoning: str


# Deliberately conservative: these are cheap heuristics, not real inference,
# so confidence is capped well below the 1.0 the rule table gets.
_HARD_HINTS = ("expired", "revoked", "closed", "blocked", "invalid card", "cancelled", "cancel")
_SOFT_HINTS = ("insufficient", "timeout", "network", "declined by bank", "try again", "temporary", "low balance")


def classify_via_llm(raw_reason_text: str) -> LLMClassification:
    """
    Placeholder LLM fallback. Real version prompts a single LLM with the
    raw failure text and asks for {bucket, confidence, reasoning} as
    structured JSON. For now: keyword match against known hard/soft
    decline vocabulary, defaulting to UNCERTAIN with low confidence when
    nothing matches — the safe failure mode is "ask a human", not "guess".
    """
    text = (raw_reason_text or "").lower().strip()

    if not text:
        return LLMClassification("UNCERTAIN", 0.0, "Empty/missing reason text — cannot classify.")

    if any(hint in text for hint in _HARD_HINTS):
        return LLMClassification(
            "HARD", 0.62, f"Heuristic matched hard-decline language in free text: '{raw_reason_text}'"
        )
    if any(hint in text for hint in _SOFT_HINTS):
        return LLMClassification(
            "SOFT", 0.58, f"Heuristic matched soft-decline language in free text: '{raw_reason_text}'"
        )
    return LLMClassification(
        "UNCERTAIN", 0.30, f"No confident hard/soft signal found in free text: '{raw_reason_text}'"
    )