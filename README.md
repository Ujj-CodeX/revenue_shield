# Revenue Shield AI

An operational intelligence copilot that classifies failed recurring payments, decides whether a retry is economically worth attempting, and proves the decision's value with a live, re-runnable backtest against a naive baseline.

*Built for the Razorpay Ideathon 2026 — AI Revenue Recovery Track.*

---

## Problem Statement

Recurring payments in India — UPI AutoPay, e-mandates, subscription billing — fail at structurally high rates. The default handling almost every system falls back to is one flow for every failure:

```mermaid
flowchart LR
    A[Payment Fails] --> B[Retry]
    B --> C[Retry Again]
    C --> D[Notify Merchant]

    style A fill:#2a1414,stroke:#ff5c5c,color:#fff
    style B fill:#2a1414,stroke:#ff5c5c,color:#fff
    style C fill:#2a1414,stroke:#ff5c5c,color:#fff
    style D fill:#2a1414,stroke:#ff5c5c,color:#fff
```

This treats an expired card and a same-day network blip identically. Two costs follow:

- **Merchant side** — lost revenue, no visibility into *why* payments fail, no way to prioritize which failures are worth chasing.
- **Aggregator side** — retrying a permanently dead instrument (expired card, revoked mandate) doesn't just waste a retry attempt; it inflates the aggregator's decline rate, a metric banks and card networks track per aggregator.

There is no decision layer between *"payment failed"* and *"retry it."* Revenue Shield AI is that layer.

---

## Why Existing Systems Fail

```mermaid
flowchart TD
    subgraph naive["Naive retry-everything system"]
        direction TB
        N1[Failure event] --> N2{Any distinction<br/>between failure types?}
        N2 -->|No| N3[Retry blindly]
        N3 --> N4[Dead cards retried<br/>forever]
        N3 --> N5[Decline rate rises]
    end

    subgraph shield["Revenue Shield AI"]
        direction TB
        S1[Failure event] --> S2{Classify:<br/>HARD / SOFT / UNCERTAIN}
        S2 -->|HARD| S3[No retry.<br/>Auditable ops report]
        S2 -->|SOFT| S4{Expected Value ≥ 0?}
        S4 -->|No| S5[Skip and flag]
        S4 -->|Yes| S6[Time it, check bank health,<br/>simulate retry, log outcome]
        S2 -->|UNCERTAIN| S7[Below-confidence →<br/>human review, not forced]
    end
```

---

## Solution Overview

**In business terms:** before spending a retry attempt, the system asks two questions — *is this actually recoverable*, and *is it worth the cost of trying*. Dead instruments (expired cards, revoked mandates) are reported for merchant/ops action instead of retried. Everything else is scored on expected value before a retry is scheduled.

**In technical terms:** a rule table classifies structured gateway reason codes for free; an LLM (Groq) is invoked only for the minority of unstructured/unknown reason text; an Expected-Value Gate (`P(recover) × amount − retry_cost`) decides whether a retry is scheduled; a cross-customer z-score scan detects when a bank is systemically degraded and reschedules around it; and a backtest engine re-runs both this policy and a naive "retry everything" baseline against the same synthetic dataset to produce a directly comparable ₹-recovered number.

The system never touches a live payment flow. It is advisory — it classifies, decides, and reports.

---

## End-to-End Product Flow

This is the actual frontend state machine (`App.vue`) plus what one API call (`GET /api/dashboard/`) triggers server-side.

```mermaid
flowchart TD
    U([User opens app]) --> Hero[Hero Screen]
    Hero --> Select[Merchant Selection]
    Select --> Loading[Loading Overlay<br/>cosmetic pacing]
    Loading -->|GET /api/dashboard/?merchant_id&seed| Pipeline

    subgraph Pipeline["Server-side pipeline — one request"]
        direction TB
        P1[Generate synthetic<br/>failure events] --> P2[Classify each event<br/>Hard / Soft / Uncertain]
        P2 --> P3[Detect systemic<br/>bank degradation]
        P3 --> P4[Expected-Value Gate<br/>+ retry timing]
        P4 --> P5[Run backtest:<br/>Policy arm vs Naive arm]
        P5 --> P6[Persist BacktestRun<br/>+ audit log entry]
    end

    Pipeline --> Dashboard[Dashboard renders:<br/>KPIs, failed payments table,<br/>bucket summary, hard-decline report,<br/>backtest panel]
    Dashboard -->|Re-run Backtest button| Rerun[New seed →<br/>GET /api/backtest/run/]
    Rerun --> Pipeline
    Dashboard -->|Export| CSV[Hard-decline CSV<br/>download]
```

Nothing on the dashboard is precomputed or hardcoded — every figure is produced by that one request, and pressing **Re-run Backtest** genuinely reruns the pipeline with a fresh seed.

---

## System Architecture

Seven Django apps, one of which (`ops_console`) is the only app the frontend talks to; it orchestrates the other six.

```mermaid
flowchart TB
    FE["Frontend — Vue 3<br/>Hero → Select → Loading → Dashboard"]

    FE -->|REST/JSON| OPS

    subgraph backend["Django backend"]
        OPS["ops_console/<br/>orchestrator + CSV export<br/>(the only app the frontend calls)"]
        SIM["simulator/<br/>synthetic customers + mock gateway<br/>emits ObservableEvent only"]
        CLS["classification/<br/>rule table + Groq LLM fallback<br/>HARD / SOFT / UNCERTAIN + confidence"]
        POL["policy/<br/>EV Gate + retry timing +<br/>bank-degradation detection"]
        BT["backtest/<br/>policy arm vs naive arm,<br/>persists BacktestRun"]
        AUD["audit/<br/>immutable, append-only<br/>AuditLogEntry"]
        DB[(PostgreSQL / SQLite)]
    end

    OPS --> SIM
    OPS --> CLS
    OPS --> POL
    OPS --> BT
    BT --> AUD
    SIM --> DB
    BT --> DB
    AUD --> DB
```

**Note on scope:** `audit/logger.py` provides `log_classification()` and `log_policy_decision()` helpers, but in the current wiring only `log_backtest_run()` is actually called (from `backtest.persist_backtest_run`). Per-event classification and EV-gate decisions are *not* currently written to the audit log during a live dashboard request — see [Limitations](#limitations).

---

## Data Flow Diagram

The core architectural rule of the codebase: `classification/` and `policy/` may only see `ObservableEvent` rows. `SyntheticCustomer` (the hidden ground truth — balance timeline, salary date, card/mandate validity) is queried only by the simulator itself and by the backtest, which needs it to grade outcomes.

```mermaid
flowchart LR
    GT[("SyntheticCustomer<br/>hidden ground truth<br/>(backtest-only)")]
    GW[MockGateway]
    OE[("ObservableEvent<br/>customer_id, timestamp,<br/>amount, reason_code, bank")]

    GT -->|resolved by| GW
    GW -->|emits| OE

    OE --> CLS[Classification]
    CLS -->|bucket + confidence| POL[Policy Decision<br/>EV Gate + timing]
    POL -->|approved retries only| REC[Recovery Simulation<br/>vs fresh MockGateway]
    REC --> DASH[Dashboard payload]
    GT -.->|grading only, never exposed<br/>to classification/policy| BT[Backtest comparison]
    REC --> BT
    BT --> DASH
```

---

## Classification Pipeline

Rule-first, LLM-fallback — not multi-model. Structured reason codes are the majority case and are resolved by a zero-cost lookup table; the LLM (Groq, `llama-3.1-8b-instant`) is called only when the reason code is `UNKNOWN_DECLINE` or otherwise unrecognized.

```mermaid
flowchart TD
    E["Observable event<br/>{reason_code, raw_text, amount}"] --> K{Known structured<br/>reason_code?}

    K -->|Yes| R["Rule table lookup<br/>(reason_lookup.py)<br/>confidence = 1.0, instant, free"]
    K -->|No / UNKNOWN_DECLINE| L["Groq LLM fallback<br/>(llm_fallback.py)<br/>reads raw_text"]

    L -->|timeout or API error| F["LLMTimeoutError caught →<br/>confidence = 0.0, UNCERTAIN<br/>(never a silent guess)"]

    R --> C{confidence <<br/>threshold 0.5?}
    L --> C
    F --> C

    C -->|Yes| U[UNCERTAIN → flagged<br/>for human review]
    C -->|No| B[HARD or SOFT<br/>bucket assigned]
```

---

## Expected-Value Gate

```mermaid
flowchart TD
    IN["Classified event:<br/>bucket, confidence, amount"] --> HB{Bucket = HARD?}
    HB -->|Yes| NO1["No retry — hard rule,<br/>not an EV outcome<br/>(never retried, regardless of math)"]
    HB -->|No| EV["EV = P(recover) × amount − retry_cost"]
    EV --> POS{EV > 0?}
    POS -->|Yes| RETRY["Retry approved →<br/>retry_timing.py picks the date<br/>(customer history → reason default → bucket fallback)"]
    RETRY --> BANK{Bank flagged as<br/>systemically degraded<br/>on that date?}
    BANK -->|Yes| PUSH["Push forward day-by-day<br/>(capped at 14 days)"]
    BANK -->|No| SCHED[Retry scheduled]
    PUSH --> SCHED
    POS -->|No| SKIP["Skip and flag —<br/>not worth the cost"]
```

`P(recover)` is a base rate per bucket (SOFT: 0.55, UNCERTAIN: 0.30 × confidence), overridden per reason code for SOFT declines (`INSUFFICIENT_FUNDS`: 0.60, `BANK_TIMEOUT`: 0.70, `NETWORK_ERROR`: 0.75). These are hand-set placeholder priors — the code documents itself as a "swap-in point" for rates learned from real retry-outcome data.

---

## Backtest Engine

```mermaid
flowchart TD
    DS[("Same synthetic dataset<br/>seed-locked, shared by both arms")]

    DS --> POLICY
    DS --> NAIVE

    subgraph POLICY["Policy arm"]
        direction TB
        PA1[Classify] --> PA2[EV Gate]
        PA2 --> PA3[Retry timing +<br/>bank-pattern reschedule]
        PA3 --> PA4["Retry ONLY events<br/>that are EV-positive"]
    end

    subgraph NAIVE["Naive arm"]
        direction TB
        NA1["No classification, no EV check"]
        NA1 --> NA2["Retry every failure,<br/>1 day later, blindly<br/>(includes dead instruments)"]
    end

    PA4 --> SIM1["Simulated against a<br/>FRESH MockGateway<br/>(same seed, same degradation window)"]
    NA2 --> SIM2["Simulated against a<br/>FRESH, independent MockGateway<br/>(same seed, same degradation window)"]

    SIM1 --> CMP["Comparison Report:<br/>₹ recovered, useless retries avoided,<br/>attempts, success rate"]
    SIM2 --> CMP
    CMP --> PERSIST[("BacktestRun row<br/>+ audit log entry")]
```

Both arms are simulated against independently-constructed `MockGateway` instances seeded identically to the original dataset's gateway, so neither arm can "consume" stochastic luck meant for the other. The only thing that legitimately differs between the two arms is *which* events get retried and *when* — the two decisions the policy layer claims to make better than blind retrying.

---

## Component Responsibility Matrix

| Component | Purpose | Input | Output |
|---|---|---|---|
| `simulator/` | Generates synthetic customers with hidden ground truth; resolves payment attempts against that ground truth via a mock gateway | seed, customer count, months | `ObservableEvent` rows (never exposes ground truth) |
| `classification/` | Buckets each event as HARD / SOFT / UNCERTAIN | `ObservableEvent` dicts | `ClassificationResult` (bucket, confidence, source, reasoning) |
| `policy/` | Decides whether to retry (EV Gate), when (retry timing), and adjusts for bank-wide degradation | `ClassificationResult` + event's `bank` field | `PolicyDecision` (final retry date or none, audit trail) |
| `backtest/` | Runs the policy arm and a naive "retry everything" arm against the same dataset and compares recovered ₹ | seed, customer count, months, optional merchant filter | `BacktestReport`, persisted `BacktestRun` |
| `audit/` | Append-only log of decisions (rows are immutable by construction — `save()` rejects updates) | Objects from classification/policy/backtest | `AuditLogEntry` rows (currently only backtest runs are logged in the live flow) |
| `ops_console/` | Wires the pipeline together into one dashboard payload; exposes the only endpoints the frontend calls; builds hard-decline CSV export | HTTP query params (`merchant_id`, `seed`, etc.) | JSON dashboard payload / CSV file |
| `ingestion/` | Django app scaffold for accepting failure events in a webhook-like shape | — | Models only; no active views wired into the live pipeline |

---

## API Surface

| Endpoint | Method | Description |
|---|---|---|
| `/api/merchants/` | `GET` | Returns the 5 synthetic merchants (`MERCH_001`–`MERCH_005`) available for selection |
| `/api/dashboard/?merchant_id=&seed=&n_customers=&months=` | `GET` | Runs the full pipeline live — generate → classify → EV-gate → backtest — and returns the dashboard payload |
| `/api/backtest/run/?merchant_id=&seed=` | `GET` / `POST` | Powers "Re-run Backtest"; same pipeline, typically a fresh seed |
| `/api/hard-declines/export?merchant_id=&seed=` | `GET` | Downloadable CSV of HARD-bucket customers (`customer_id`, `payment_amount`, `failure_reason`, `confidence`, `recommended_action`) |

Query defaults: `seed=42`, `n_customers=200`, `months=4`. `merchant_id` is optional — omitting it runs the pipeline platform-wide across all synthetic merchants.

The frontend (`services/api.js`) calls these endpoints and falls back to a lightweight, clearly-labeled client-side simulator (`services/simulator.js`) if the backend is unreachable, so the demo UI doesn't hard-crash on a network blip during a live presentation.

---

## Screenshots

> Replace with actual captures before submission.

| Screen | Placeholder |
|---|---|
| Hero Screen | `docs/screenshots/hero.png` |
| Merchant Selection | `docs/screenshots/merchant-select.png` |
| Classification / Failed Payments Table | `docs/screenshots/classification-results.png` |
| Hard-Decline CSV Export | `docs/screenshots/csv-export.png` |
| Backtest Results Panel | `docs/screenshots/backtest-results.png` |
| Full Dashboard | `docs/screenshots/dashboard.png` |

---

## Technical Decisions

**Why rule-first classification?** Gateway failure reason codes are structured in the large majority of real cases. A lookup table classifies these instantly, at zero cost, with a fully inspectable reason. Running an LLM on every event would add latency and cost for no accuracy gain on the easy majority.

**Why LLM fallback, not LLM-first or multi-model?** The LLM (Groq) is invoked only when the reason code is `UNKNOWN_DECLINE` or not a known enum value — the genuinely ambiguous minority. If the Groq call times out or errors, the classifier catches `LLMTimeoutError` and routes the event to `UNCERTAIN` with `confidence = 0.0` rather than guessing — this is enforced in code (`_safe_llm_classify`), not just documentation.

**Why synthetic data instead of a public dataset?** No public dataset exposes ground truth for "would this specific payment have succeeded on a retry" — that information is exactly what a real aggregator would never share externally. Generating hidden ground truth (balance timeline, card/mandate validity) and only exposing an `ObservableEvent` view of it lets the classifier and policy layers be graded against a real answer key while being architecturally restricted to the same information a production system would actually have.

**Why backtesting against a naive baseline?** A predicted-recovery number is not evidence of anything by itself. Running a second, naive "retry everything" policy against the *same* synthetic dataset — same customers, same gateway seed, same degradation window — produces a directly comparable ₹-recovered figure, which is the difference between claiming impact and measuring it.

---

## Limitations

Stated explicitly, per the problem statement's own scope boundary (Section 4) and verified against the current codebase:

- **Does not touch the live payment flow, bank, or NPCI processing.** The simulator's `MockGateway` is the only "gateway" in this system.
- **Does not handle transaction authorization** and **does not message customers directly** — hard-decline output is a CSV/report for ops/merchant action, not an automated notification.
- **JWT authentication and RBAC are not implemented.** The problem statement's technical-architecture section describes per-firm JWT/RBAC logins as part of the intended design; the current codebase has no auth app, no `rest_framework_simplejwt` dependency, and no `IsAuthenticated`/permission classes anywhere in the views. All API endpoints are currently open.
- **Celery, Redis, and Docker are not present in the repository.** The problem statement's architecture table lists these as the intended async/deployment layer; the current implementation runs the entire pipeline synchronously inside a single Django request, with no `Dockerfile`, `docker-compose.yml`, or Celery/Redis dependency in the codebase. This makes the "computed live, nothing precomputed" property easy to verify, but it also means there's no background job queue yet.
- **Per-event audit logging is partially wired.** `audit/logger.py` defines `log_classification()` and `log_policy_decision()`, but neither is currently called anywhere in the live pipeline — only `log_backtest_run()` is invoked (from `backtest.persist_backtest_run`). The audit trail today records backtest runs, not individual classification or EV-gate decisions.
- **Test suite has a known collection failure.** `pytest` (run from `backend/`) passes 34/34 collectible tests, but two test modules — `policy/tests/test_bank_pattern_detection.py` and `policy/tests/test_retry_timing.py` — fail to *collect* due to absolute imports (`import bank_pattern_detection`, `from ev_gate import Bucket`) instead of relative/package imports, and are currently skipped by `--ignore` rather than fixed.
- **Retry-recovery probabilities are hand-set priors**, not learned from real outcome data (the code documents this explicitly as a "swap-in point" for future work).
- **The `ingestion/` app is a scaffold.** It defines models but has no active view wired into the live pipeline; synthetic events are generated directly by `simulator/`, not ingested through this app.
- **No multi-tenant merchant-facing UI** — this is explicitly an internal ops tool, not something merchants log into directly.

---

## Future Scope

Realistic next steps, in rough priority order:

1. Fix the two broken test modules (import style) so the full suite collects and runs in one command.
2. Wire `log_classification()` and `log_policy_decision()` into the live `/api/dashboard/` request path so the audit trail covers every stage, not just backtest runs.
3. Add JWT authentication and DRF permission classes so per-firm ops logins actually restrict merchant visibility, as originally scoped.
4. Move the pipeline's per-request computation into a Celery task with Redis as the broker, so a large `n_customers`/`months` run doesn't block the request thread.
5. Replace the hand-set `BUCKET_BASE_RECOVERY_RATE` / `REASON_RECOVERY_RATE_OVERRIDE` constants with rates learned from accumulated `BacktestRun` history.
6. Containerize with Docker Compose (Django + Postgres + Redis) for a one-command judge setup.

---

## Running It Locally

```bash
# Backend
cd backend
pip install django djangorestframework django-cors-headers pytest pytest-django requests
python manage.py migrate
python manage.py runserver

# Frontend (separate terminal)
cd frontend/Revenue-shield
npm install
npm run dev
```

Open the frontend dev server, click through Hero → Merchant Selection, and the dashboard renders from a live `GET /api/dashboard/` call. Optional: set `GROQ_API_KEY` in `backend/.env` to enable the LLM fallback path for `UNKNOWN_DECLINE` events; without it, those events fail safe into `UNCERTAIN`.

---

## Conclusion

Revenue Shield AI does not retry every failure and count that as recovery. It classifies each failure against a rule table with an LLM fallback for the ambiguous minority, spends retry effort only where the expected value is positive, and backs every number on its dashboard with a backtest that is computed fresh on each request rather than hardcoded. The gaps that remain — authentication, background job processing, full audit coverage, a fully green test suite — are documented above rather than glossed over, because a system that can't be honest about its own limitations undermines the same "provable, not predicted" claim it's built around.
