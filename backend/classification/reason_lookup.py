

from __future__ import annotations

from simulator.reason_codes import HARD_CODES, SOFT_CODES, UNCERTAIN_CODES, ReasonCode

# Rule-table lookup is authoritative and deterministic -> always full confidence.
RULE_CONFIDENCE = 1.0


def bucket_for_reason_code(code: ReasonCode) -> str:
    """Returns 'HARD', 'SOFT', or 'UNCERTAIN' for a known ReasonCode enum member."""
    if code in HARD_CODES:
        return "HARD"
    if code in SOFT_CODES:
        return "SOFT"
    if code in UNCERTAIN_CODES:
        return "UNCERTAIN"
    # Should be unreachable if ReasonCode/HARD_CODES/SOFT_CODES/UNCERTAIN_CODES
    # stay in sync, but fail loudly rather than silently misclassify.
    raise ValueError(f"ReasonCode {code!r} is not assigned to any bucket in reason_codes.py")


_REASONING = {
    ReasonCode.CARD_EXPIRED: "Card expired — instrument is permanently dead, requires customer re-entry.",
    ReasonCode.MANDATE_REVOKED: "Mandate revoked by customer/bank — no further attempts will succeed.",
    ReasonCode.ACCOUNT_CLOSED: "Account closed — instrument is permanently invalid.",
    ReasonCode.INSUFFICIENT_FUNDS: "Insufficient balance at attempt time — commonly transient, high recovery odds.",
    ReasonCode.BANK_TIMEOUT: "Bank-side timeout — often systemic, check for a concurrent bank degradation window.",
    ReasonCode.NETWORK_ERROR: "Transient network/gateway error — typically resolves on near-immediate retry.",
    ReasonCode.UNKNOWN_DECLINE: "Reason code not structured/recognised — routed to LLM fallback.",
}


def reasoning_for_reason_code(code: ReasonCode) -> str:
    return _REASONING.get(code, f"No canned reasoning for {code!r}.")