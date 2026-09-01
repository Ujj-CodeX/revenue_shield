from django.urls import path

from .views import dashboard, rerun_backtest

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("backtest/run/", rerun_backtest, name="rerun_backtest"),
]