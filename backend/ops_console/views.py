from rest_framework.decorators import api_view
from rest_framework.response import Response

from simulator.ground_truth import MERCHANTS

from .services import build_dashboard_payload


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