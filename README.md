# 🛡️ Revenue Shield AI

**An Operational Intelligence Copilot for Recurring Payment Recovery**
*Razorpay Ideathon 2026 — AI Revenue Recovery Track*

[![Backend](https://img.shields.io/badge/backend-Django%20REST-092E20?logo=django)](.)
[![Frontend](https://img.shields.io/badge/frontend-Vue%203-4FC08D?logo=vuedotjs)](.)
[![Tests](https://img.shields.io/badge/tests-57%2F57%20passing-brightgreen)](.)
[![LLM](https://img.shields.io/badge/LLM-Groq%20(fallback%20only)-orange)](.)
[![Status](https://img.shields.io/badge/status-live%20%26%20re--runnable-blue)](.)

> Revenue Shield AI doesn't retry every failed payment and call it recovery.
> It **diagnoses before it acts**, spends recovery effort only where it's
> mathematically justified, and — unlike a dashboard of projected numbers —
> **proves its impact with a live, re-runnable backtest** against a naive baseline.

---

## 📌 The Problem, In One Picture

```
                    TODAY (every other system)
   ┌──────────────┐    ┌───────┐    ┌─────────────┐    ┌──────────────┐
   │ Payment Fails│───▶│ Retry │───▶│ Retry Again │───▶│Notify Merchant│
   └──────────────┘    └───────┘    └─────────────┘    └──────────────┘
        Every failure treated the same. Dead cards get retried.
           Decline rates rise. Razorpay's standing takes the hit.


                    REVENUE SHIELD AI
   ┌──────────────┐    ┌───────────────┐    ┌────────────────────┐
   │ Payment Fails│───▶│ Is this even  │─No▶│ HARD → No retry.    │
   │              │    │ recoverable?  │    │ Auditable report to │
   └──────────────┘    └───────┬───────┘    │ ops. Done.          │
                                │Yes         └────────────────────┘
                                ▼
                     ┌─────────────────────┐
                     │ Is it WORTH it?      │
                     │ EV = P(recover)×amt  │─No──▶ Skip & flag.
                     │      − retry_cost     │
                     └──────────┬────────────┘
                                │Yes
                                ▼
                     ┌─────────────────────┐
                     │ Time it, check bank  │
                     │ health, simulate the │
                     │ retry, log everything│
                     └─────────────────────┘
```

---

## 🔄 End-to-End Flow (What Actually Happens On "Start Analysis")

```
 ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
 │  1. HERO   │──▶│ 2. SELECT  │──▶│ 3. STAGED  │──▶│ 4. LIVE    │──▶│ 5. DASHBOARD│
 │   SCREEN   │   │  MERCHANT  │   │  LOADING   │   │  COMPUTE   │   │   RENDERS   │
 └────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
                                          │                 │
                          "Loading merchant data..."        │
                          "Generating failure scenarios..." │
                          "Running policy engine..."   ◀────┘
                          "Comparing vs naive baseline..."
                                          │
                    (cosmetic pacing — the real backend call underneath
                     is a single GET /api/dashboard/?merchant_id=X&seed=Y)
```

**🔑 Nothing on screen is precomputed.** Every ₹ figure, every bucket count, every
retry recommendation is generated fresh, live, on that one API call.

---

## 🏗️ System Architecture — The 7 Django Apps

```
                              ┌─────────────────────────┐
                              │      FRONTEND (Vue 3)    │
                              │  Hero → Merchant Select   │
                              │  → Loading → Dashboard    │
                              └────────────┬─────────────┘
                                           │ REST (JSON)
                                           ▼
                              ┌─────────────────────────┐
                              │   ops_console/  🧩       │
                              │   (the ONLY app the      │
                              │    frontend ever talks   │
                              │    to — orchestrator)     │
                              └────────────┬─────────────┘
                                           │
        ┌──────────────────┬──────────────┼──────────────┬──────────────────┐
        ▼                  ▼              ▼              ▼                  ▼
┌───────────────┐  ┌───────────────┐┌───────────────┐┌───────────────┐┌──────────────┐
│  simulator/ 🎲 │  │classification/││   policy/  ⚖️  ││ backtest/ 📊  ││  audit/ 🔒    │
│               │  │      🧠        ││               ││               ││               │
│ Fake customers│─▶│ Rule table +   │─▶│ EV Gate +     │─▶│ Policy vs    ││ Immutable log │
│ + fake payment│  │ Groq LLM       ││ retry timing +││ Naive         ││ of every       │
│ failures.     │  │ fallback (only ││ bank-outage    ││ baseline,     ││ decision made  │
│ Hidden ground │  │ for messy/     ││ detection.     ││ compared      ││ — never edited,│
│ truth is never│  │ unknown text). │ Decides:       ││ side-by-side. ││ only appended. │
│ leaked out.   │  │ Buckets:       ││ retry or not,  ││ Re-runnable   ││                │
│               │  │ HARD/SOFT/     ││ and when.      ││ on demand.    ││                │
│               │  │ UNCERTAIN      ││               ││               ││               │
└───────────────┘  └───────────────┘└───────────────┘└───────────────┘└──────────────┘
```

---

## 🎯 The Classification Logic (Section 6 of the Problem Statement)

```
                     Observable Failure Event
                    {reason_code, raw_text, amount}
                              │
                              ▼
                  ┌───────────────────────┐
                  │ Is reason_code a known │
                  │ structured code?       │
                  └───────┬───────┬───────┘
                     Yes  │       │  No / UNKNOWN_DECLINE
                          ▼       ▼
              ┌───────────────┐ ┌────────────────────────┐
              │  RULE TABLE   │ │   GROQ LLM FALLBACK      │
              │  (instant,    │ │   (only for the messy    │
              │   free,       │ │    minority — reads       │
              │   confidence  │ │    raw_text like "txn     │
              │   = 1.0)      │ │    declined by issuer")   │
              └───────┬───────┘ └────────────┬────────────┘
                      │                       │
                      └───────────┬───────────┘
                                  ▼
                    ┌──────────────────────────┐
                    │ confidence < threshold?   │
                    └─────┬────────────────┬────┘
                       Yes │                │ No
                           ▼                ▼
                 ┌──────────────┐   ┌──────────────────┐
                 │  UNCERTAIN    │   │  HARD  or  SOFT   │
                 │  → flagged    │   │  bucket assigned   │
                 │  for human    │   └──────────────────┘
                 │  review        │
                 └──────────────┘
```

> 🧠 **Why rule-first, not LLM-first?** Structured reason codes are already
> the large majority of gateway responses — a lookup table classifies them
> instantly, for free, with full explainability. The LLM is invoked **only**
> for the genuinely ambiguous minority. This keeps the system fast, cheap,
> and auditable — and if Groq times out, `_safe_llm_classify()` fails safe
> into UNCERTAIN rather than crashing the pipeline.

---

## 💰 The Expected-Value Gate (Section 6.4)

```
        expected_value = P(recover) × payment_amount − retry_cost

                    ┌─────────────────────┐
                    │   EV > 0 ?            │
                    └────┬─────────────┬────┘
                     Yes │             │ No
                         ▼             ▼
              ┌────────────────┐  ┌──────────────────┐
              │  ✅ ATTEMPT      │  │  ⛔ SKIP & FLAG    │
              │  RETRY           │  │  (not worth the   │
              │                 │  │  operational /     │
              │  → check bank   │  │  decline-rate      │
              │    health       │  │  cost)             │
              │  → time it      │  └──────────────────┘
              │    right        │
              │  → simulate it  │
              │  → log it       │
              └────────────────┘
```

---

## 📊 The Proof Engine — Backtest (Section 7, the core differentiator)

```
                    Same Synthetic Dataset (seed-locked)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
   ┌─────────────────────┐        ┌─────────────────────┐
   │   POLICY ARM          │        │    NAIVE ARM          │
   │   (Revenue Shield)     │        │   (retry everything)   │
   │                       │        │                       │
   │  Classify → EV Gate →  │        │  No classification.    │
   │  Time it → Simulate    │        │  No EV check. Retry     │
   │  only EV-positive      │        │  every single failure   │
   │  retries.               │        │  once, blindly.          │
   └───────────┬───────────┘        └───────────┬───────────┘
               │                                 │
               └────────────────┬────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │   COMPARISON REPORT       │
                    │  ₹ recovered (both arms)   │
                    │  useless retries avoided   │
                    │  precision / recall         │
                    └─────────────────────────┘

   📈 LIVE RESULT (seed=42, 200 customers, 4 months, 112 failures):

   ┌───────────────────────┬─────────────┬─────────────┐
   │                       │  POLICY      │   NAIVE       │
   ├───────────────────────┼─────────────┼─────────────┤
   │ Retries attempted     │     63       │     112       │
   │ ₹ Recovered            │   ₹33,257    │   ₹25,970     │
   │ Useless retries avoided│     75.6%    │      —        │
   └───────────────────────┴─────────────┴─────────────┘

   → +29% more revenue recovered, using 44% FEWER retries.
   → Every one of those numbers is computed live — click
     "Re-run Backtest" and watch a new seed produce a new,
     honest result. Nothing here is hardcoded.
```

---

## 🌐 API Surface (the only 4 endpoints the frontend needs)

| Endpoint | Method | What it does |
|---|---|---|
| `/api/merchants/` | `GET` | List of synthetic merchants to analyze |
| `/api/dashboard/?merchant_id=&seed=` | `GET` | Runs the **entire pipeline live** — simulate → classify → EV-gate → backtest — and returns the dashboard payload |
| `/api/backtest/run/?merchant_id=&seed=` | `GET`/`POST` | Powers the "Re-run Backtest" button — same pipeline, fresh seed |
| `/api/hard-declines/export?merchant_id=&seed=` | `GET` | Downloadable CSV of HARD-decline customers for ops action |

---

## 🧱 Tech Stack

```
┌─────────────────────────────┐        ┌─────────────────────────────┐
│         BACKEND               │        │          FRONTEND             │
├─────────────────────────────┤        ├─────────────────────────────┤
│ Django + Django REST Framework│        │ Vue 3 (Options API)           │
│ SQLite (dev) / PostgreSQL-ready│        │ Plain JS, no TypeScript        │
│ pytest — 57/57 tests passing  │        │ Bootstrap + custom terminal CSS│
│ Groq (LLM fallback only)      │        │ Dark, monospace, Stripe/Linear-│
│ django-cors-headers           │        │ inspired ops-console aesthetic │
└─────────────────────────────┘        └─────────────────────────────┘
```

---

## 🚀 Running It Locally

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

Open `http://localhost:3000` → **Start Analysis** → pick a merchant → watch the
pipeline run live.

---

## ✅ What This Project Deliberately Does NOT Do

*(a trust decision, not a limitation — Section 4 of the problem statement)*

- ❌ Does not touch the live payment flow, bank, or NPCI processing
- ❌ Does not handle transaction authorization
- ❌ Does not message customers directly — delivery is an ops/merchant action
- ❌ Does not force a bucket decision when confidence is low — routes to human review instead

---

## 🏁 Closing Line

> Every number on this dashboard — revenue at risk, recoverable revenue,
> useless retries avoided — is computed by a real pipeline against real
> (synthetic) data, every single time you press a button. That's the bet
> this project makes: **not a prediction dashboard, a provable one.**
