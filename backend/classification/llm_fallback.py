"""
llm_fallback.py — Groq (free tier) classifier. Called FIRST by classifier.py.
Raises LLMTimeoutError on timeout/failure so the caller falls back to the
rule table — never silently guesses.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

import requests

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_TIMEOUT_SECONDS = float(os.environ.get("GROQ_TIMEOUT_SECONDS", "4"))

SYSTEM_PROMPT = (
    "Classify a failed recurring payment's reason into exactly one bucket. "
    "HARD = dead instrument (expired card, revoked mandate, closed account), never retry. "
    "SOFT = temporary (insufficient funds, bank timeout, network error), retry-eligible. "
    "UNCERTAIN = unclear reason. "
    'Reply ONLY as JSON: {"bucket": "HARD|SOFT|UNCERTAIN", "confidence": 0.0-1.0, "reasoning": "..."}'
)


class LLMTimeoutError(Exception):
    pass


@dataclass
class LLMClassification:
    bucket: str
    confidence: float
    reasoning: str


def classify_via_llm(raw_text: str) -> LLMClassification:
    if not GROQ_API_KEY:
        raise LLMTimeoutError("GROQ_API_KEY not set")
    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Reason: {raw_text}"},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0,
            },
            timeout=GROQ_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        parsed = json.loads(resp.json()["choices"][0]["message"]["content"])
        bucket = str(parsed.get("bucket", "")).upper()
        if bucket not in ("HARD", "SOFT", "UNCERTAIN"):
            bucket = "UNCERTAIN"
        return LLMClassification(
            bucket=bucket,
            confidence=float(parsed.get("confidence", 0.5)),
            reasoning=parsed.get("reasoning", "LLM classification"),
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        raise LLMTimeoutError(f"Groq timeout: {e}") from e
    except (requests.exceptions.RequestException, KeyError, ValueError, json.JSONDecodeError) as e:
        raise LLMTimeoutError(f"Groq call failed: {e}") from e