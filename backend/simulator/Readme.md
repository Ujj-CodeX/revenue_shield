# Revenue Shield AI — Stage 0: Synthetic Data Generator + Mock Gateway

## Run the demo
    cd revenue_shield
    python3 -m simulator.generator

## Run the tests
    pip install pytest --break-system-packages
    python3 -m pytest tests/test_simulator.py -v

## Files
- `simulator/reason_codes.py`  — reason-code taxonomy (mirrors Razorpay's real documented decline codes)
- `simulator/ground_truth.py`  — hidden customer state (balance timeline, card/mandate validity) — never exposed downstream
- `simulator/gateway.py`       — mock gateway: resolves attempt_payment() against ground truth, emits ONLY the observable event
- `simulator/generator.py`     — orchestrator: builds population + degradation window + walks calendar to produce the event stream
- `tests/test_simulator.py`    — reproducibility, ground-truth isolation, and decline-priority tests

## Design rule this stage enforces
The classifier/policy engine (next stage) will only ever see:
  {customer_id, timestamp, amount, reason_code}
Never salary_day, balance, card_valid_until, etc. — that stays inside the
simulator, exactly like Razorpay never sees a customer's actual bank ledger.