"""
Persistence layer for the simulator app.

Two tables are deliberately kept apart, matching the isolation rule from
Stage 0:

  - SyntheticCustomer -> hidden ground truth. Only backtest/audit code
    should ever query this table directly.
  - ObservableEvent    -> what classification/policy actually consume.
    This is the equivalent of a real Razorpay failure webhook payload.

A SimulationRun ties a seed + params to the records it produced, so a
backtest can be re-run and compared against a previous run by seed.
"""

from django.db import models


class SimulationRun(models.Model):
    seed = models.IntegerField()
    n_customers = models.IntegerField()
    months = models.IntegerField()
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Run(seed={self.seed}, n={self.n_customers}, months={self.months})"


class SyntheticCustomer(models.Model):
    """Hidden ground truth — for backtest grading and audit only."""

    run = models.ForeignKey(SimulationRun, on_delete=models.CASCADE, related_name="customers")
    customer_id = models.CharField(max_length=32)
    bank = models.CharField(max_length=32)

    subscription_amount = models.FloatField()
    due_day = models.IntegerField()

    starting_balance = models.FloatField()
    salary_day = models.IntegerField()
    salary_amount = models.FloatField()
    daily_burn = models.FloatField()

    card_valid_until = models.DateField(null=True, blank=True)
    mandate_revoked_on = models.DateField(null=True, blank=True)
    account_closed_on = models.DateField(null=True, blank=True)

    base_network_error_rate = models.FloatField(default=0.03)

    class Meta:
        unique_together = ("run", "customer_id")

    def __str__(self):
        return f"{self.customer_id} (run {self.run_id})"


class ObservableEvent(models.Model):
    run = models.ForeignKey(SimulationRun, on_delete=models.CASCADE, related_name="events")
    customer_id = models.CharField(max_length=32)
    timestamp = models.DateField()
    amount = models.FloatField()
    reason_code = models.CharField(max_length=32)
    raw_text = models.CharField(max_length=255, null=True, blank=True)  # only set when reason_code == UNKNOWN_DECLINE
    bank = models.CharField(max_length=32,default="UNKNOWN")

    class Meta:
        indexes = [
            models.Index(fields=["run", "reason_code"]),
            models.Index(fields=["run", "customer_id"]),
        ]

class EventGroundTruth(models.Model):
    """
    Backtest-only. True reason behind each ObservableEvent — deliberately
    a separate table so classification/policy code has no query path that
    could accidentally reach it. Only backtest/grading code should import
    this model.
    """
    run = models.ForeignKey(SimulationRun, on_delete=models.CASCADE, related_name="event_truths")
    event = models.OneToOneField(ObservableEvent, on_delete=models.CASCADE, related_name="ground_truth")
    true_reason_code = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.event_id} -> {self.true_reason_code}"    