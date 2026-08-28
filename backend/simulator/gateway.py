"""
gateway.py

The mock payment gateway. This is the ONLY place allowed to look at a
customer's hidden ground truth. Everything it returns to the caller is
exactly what a real Razorpay-style webhook would contain: an outcome
(SUCCESS/FAIL) plus a categorised reason code — never raw balance,
salary date, or instrument details.

Also owns "systemic bank degradation" — a scripted event where one bank's
timeout rate spikes for a window of days, so the classification/policy
layers have a genuine cross-customer pattern to detect later.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date

from .ground_truth import CustomerGroundTruth
from .reason_codes import ReasonCode


@dataclass
class PaymentOutcome:
    customer_id: str
    timestamp: date
    amount: float
    success: bool
    reason_code: ReasonCode | None
    bank: str = ""                          # NEW — observable, same as a real webhook's bank/gateway field
    raw_text: str | None = None
    true_reason_code: ReasonCode | None = None

@dataclass
class BankDegradationWindow:
    bank: str
    start: date
    end: date
    extra_timeout_rate: float  # added on top of base_network_error_rate

    def is_active(self, on_date: date) -> bool:
        return self.start <= on_date <= self.end


class MockGateway:
    # A small set of realistic messy/free-text strings a bank sometimes
    # returns instead of a clean code. Keyed by the TRUE underlying reason,
    # so the LLM fallback has something plausible to reason about — and the
    # backtest can later grade whether the fallback recovered the right bucket.
    MESSY_TEXT_BY_TRUE_REASON = {
        ReasonCode.INSUFFICIENT_FUNDS: [
            "txn declined by issuer - retry later",
            "do not honour - issuer declined",
            "payment could not be completed at this time",
        ],
        ReasonCode.CARD_EXPIRED: [
            "instrument not valid for this transaction",
            "issuer declined - check card details",
        ],
        ReasonCode.MANDATE_REVOKED: [
            "standing instruction no longer active",
            "authorisation withdrawn by customer",
        ],
        ReasonCode.BANK_TIMEOUT: [
            "no response from issuer, please retry",
            "processing delay at bank end",
        ],
        ReasonCode.NETWORK_ERROR: [
            "temporary technical issue, retry the payment",
        ],
        ReasonCode.ACCOUNT_CLOSED: [
            "issuer unable to process - contact your bank",
        ],
    }

    # Fraction of declines whose clean reason code gets obscured into a
    # messy free-text UNKNOWN_DECLINE event instead — this is what forces
    # the classification layer to actually use its LLM fallback path.
    UNCERTAIN_OBSCURE_RATE = 0.08

    def __init__(self, seed: int, degradation_windows: list[BankDegradationWindow] | None = None):
        self._rng = random.Random(seed)
        self.degradation_windows = degradation_windows or []

    def _active_degradation(self, bank: str, on_date: date) -> BankDegradationWindow | None:
        for w in self.degradation_windows:
            if w.bank == bank and w.is_active(on_date):
                return w
        return None

    def _decline(self, customer_id: str, on_date: date, amount: float, true_reason: ReasonCode) -> PaymentOutcome:
        """
        Emits the OBSERVABLE outcome for a decline. Most of the time this
        just passes the true reason code straight through (matching the
        documented Razorpay behaviour where structured codes ARE returned).
        A small fraction get obscured into an UNKNOWN_DECLINE + free text —
        modelling the minority of cases where the bank/network returns
        something unstructured instead.
        """
        if self._rng.random() < self.UNCERTAIN_OBSCURE_RATE and true_reason in self.MESSY_TEXT_BY_TRUE_REASON:
            text = self._rng.choice(self.MESSY_TEXT_BY_TRUE_REASON[true_reason])
            return PaymentOutcome(
                customer_id, on_date, amount, False,
                reason_code=ReasonCode.UNKNOWN_DECLINE, raw_text=text, true_reason_code=true_reason,
            )
        return PaymentOutcome(
            customer_id, on_date, amount, False,
            reason_code=true_reason, raw_text=None, true_reason_code=true_reason,
        )

    def attempt_payment(self, customer: CustomerGroundTruth, on_date: date) -> PaymentOutcome:
        """
        Resolves a single payment attempt against the customer's hidden
        ground truth. Priority order matches how a real gateway would
        actually fail a transaction: dead instrument first (no point
        checking balance on an expired card), then systemic issues, then
        balance, then a small residual chance of a transient blip even on
        an otherwise healthy attempt.
        """
        amount = customer.subscription_amount

        # 1. Permanently dead instrument -> hard decline, balance irrelevant.
        if customer.is_card_expired(on_date):
            return self._decline(customer.customer_id, on_date, amount, ReasonCode.CARD_EXPIRED)
        if customer.is_mandate_revoked(on_date):
            return self._decline(customer.customer_id, on_date, amount, ReasonCode.MANDATE_REVOKED)
        if customer.is_account_closed(on_date):
            return self._decline(customer.customer_id, on_date, amount, ReasonCode.ACCOUNT_CLOSED)

        # 2. Systemic bank degradation -> soft decline, not the customer's fault.
        degradation = self._active_degradation(customer.bank, on_date)
        timeout_rate = customer.base_network_error_rate + (degradation.extra_timeout_rate if degradation else 0.0)
        if self._rng.random() < timeout_rate:
            reason = ReasonCode.BANK_TIMEOUT if degradation else ReasonCode.NETWORK_ERROR
            return self._decline(customer.customer_id, on_date, amount, reason)

        # 3. Balance check -> the everyday soft decline.
        if customer.balance_on(on_date) < amount:
            return self._decline(customer.customer_id, on_date, amount, ReasonCode.INSUFFICIENT_FUNDS)

        # 4. Otherwise, success.
        return PaymentOutcome(customer.customer_id, on_date, amount, True, None)