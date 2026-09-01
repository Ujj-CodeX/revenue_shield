from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import build_dashboard_payload


@api_view(["GET"])
def dashboard(request):
    seed = int(request.GET.get("seed", 42))
    n_customers = int(request.GET.get("n_customers", 200))
    months = int(request.GET.get("months", 4))
    return Response(build_dashboard_payload(seed=seed, n_customers=n_customers, months=months))

@api_view(["POST", "GET"])
def rerun_backtest(request):
    seed = int(request.GET.get("seed", request.data.get("seed", 42)) if hasattr(request, "data") else request.GET.get("seed", 42))
    n_customers = int(request.GET.get("n_customers", 200))
    months = int(request.GET.get("months", 4))
    return Response(build_dashboard_payload(seed=seed, n_customers=n_customers, months=months))