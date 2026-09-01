from django.db import models


class BacktestRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    # Reproducibility
    seed = models.IntegerField()
    n_customers = models.IntegerField(default=200)
    months = models.IntegerField(default=4)

    # Dataset summary
    total_failures = models.IntegerField()
    hard_declines_skipped = models.IntegerField(default=0)

    # Policy arm
    policy_attempts = models.IntegerField()
    policy_successes = models.IntegerField()

    policy_rupees_recovered = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    policy_retry_cost_spent = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    # Naive arm
    naive_attempts = models.IntegerField()

    naive_successes = models.IntegerField()

    naive_rupees_recovered = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    naive_retry_cost_spent = models.DecimalField(
        max_digits=14,
        decimal_places=2
    )

    # KPI
    useless_retries_avoided_pct = models.FloatField(default=0.0)

    notes = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"BacktestRun #{self.id} "
            f"(seed={self.seed})"
        )