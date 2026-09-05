"""
reason_codes.py

The set of failure reason codes the SIMULATOR is allowed to emit as an
"observable event". These mirror Razorpay's real, documented decline-reason
taxonomy (see razorpay.com/docs/errors/) — categorised buckets, not raw
account internals.

IMPORTANT DESIGN RULE (do not violate this elsewhere in the codebase):
The simulator's internal ground truth (salary day, running balance, card
expiry date, mandate status) must NEVER be attached to an emitted event.
Only a reason_code + timestamp + amount + customer_id + bank/gateway may be
observed downstream, exactly like a real Razorpay failure webhook payload.
"""

from enum import Enum


class ReasonCode(str, Enum):
    
    CARD_EXPIRED = "CARD_EXPIRED"
    MANDATE_REVOKED = "MANDATE_REVOKED"
    ACCOUNT_CLOSED = "ACCOUNT_CLOSED"

   
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    BANK_TIMEOUT = "BANK_TIMEOUT"
    NETWORK_ERROR = "NETWORK_ERROR"

    
    UNKNOWN_DECLINE = "UNKNOWN_DECLINE"



HARD_CODES = {ReasonCode.CARD_EXPIRED, ReasonCode.MANDATE_REVOKED, ReasonCode.ACCOUNT_CLOSED}
SOFT_CODES = {ReasonCode.INSUFFICIENT_FUNDS, ReasonCode.BANK_TIMEOUT, ReasonCode.NETWORK_ERROR}
UNCERTAIN_CODES = {ReasonCode.UNKNOWN_DECLINE}