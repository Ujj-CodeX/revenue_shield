from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.classification.classifier import classify_batch
from backend.simulator.generator import SyntheticDataset
from simulator.ground_truth import MERCHANTS

from .services import build_dashboard_payload

import csv
from django.http import HttpResponse


@api_view(["GET"])
def merchants(request):
    return Response(MERCHANTS)


@api_view(["GET"])
def dashboard(request):
    seed = int(request.GET.get("seed", 42))
    n_customers = int(request.GET.get("n_customers", 200))
    months = int(request.GET.get("months", 4))
    merchant_id = request.GET.get("merchant_id") or None
    return Response(build_dashboard_payload(seed=seed, n_customers=n_customers, months=months, merchant_id=merchant_id))


@api_view(["POST", "GET"])
def rerun_backtest(request):
    seed = int(request.GET.get("seed", 42))
    n_customers = int(request.GET.get("n_customers", 200))
    months = int(request.GET.get("months", 4))
    merchant_id = request.GET.get("merchant_id") or None
    return Response(build_dashboard_payload(seed=seed, n_customers=n_customers, months=months, merchant_id=merchant_id))


@api_view(["GET"])
def export_hard_declines(request):

    seed = int(request.GET.get("seed", 42))
    n_customers = int(request.GET.get("n_customers", 200))
    months = int(request.GET.get("months", 4))
    merchant_id = request.GET.get("merchant_id")

    ds = SyntheticDataset(
        seed=seed,
        n_customers=n_customers,
        months=months,
    )

    events = ds.observable_events_as_dicts()

    if merchant_id:
        events = [
            e for e in events
            if e.get("merchant_id") == merchant_id
        ]

    classifications = classify_batch(events)

    hard_rows = [
        c for c in classifications
        if c.bucket.value == "HARD"
    ]

    response = HttpResponse(
        content_type="text/csv"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="hard_declines_seed_{seed}.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "customer_id",
        "payment_amount",
        "failure_reason",
        "confidence",
        "recommended_action"
    ])

    for row in hard_rows:
        writer.writerow([
            row.customer_id,
            row.amount,
            row.reason_code,
            round(row.confidence, 2),
            "DO_NOT_RETRY"
        ])

    return response