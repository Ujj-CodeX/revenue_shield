
from __future__ import annotations

from django.db import models


class AuditLogEntry(models.Model):
    STAGE_CHOICES = [
        ("classification", "Classification"),
        ("ev_gate", "EV Gate"),
        ("retry_timing", "Retry Timing"),
        ("bank_pattern", "Bank Pattern Adjustment"),
        ("backtest", "Backtest Run"),
    ]

    customer_id = models.CharField(max_length=64, db_index=True, blank=True, default="")
    event_timestamp = models.DateField(null=True, blank=True)  # original failure date, when applicable
    stage = models.CharField(max_length=32, choices=STAGE_CHOICES, db_index=True)
    bucket = models.CharField(max_length=16, blank=True, default="")
    reason_code = models.CharField(max_length=64, blank=True, default="")
    decision_summary = models.CharField(max_length=255)  # one-line, human-readable (Action Center uses this)
    reasoning = models.TextField()  # the fuller "why" — verbatim from the module that decided
    payload = models.JSONField(default=dict, blank=True)  # structured extras: confidence, EV, dates, etc.
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["customer_id", "created_at"]),
            models.Index(fields=["stage", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"[{self.stage}] {self.customer_id or '-'} — {self.decision_summary}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError(
                "AuditLogEntry rows are immutable — create a new row to record a correction, "
                "never update an existing one."
            )
        super().save(*args, **kwargs)