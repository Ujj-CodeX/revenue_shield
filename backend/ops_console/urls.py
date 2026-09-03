from django.urls import path

from .views import dashboard, export_hard_declines, merchants, rerun_backtest

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("backtest/run/", rerun_backtest, name="rerun_backtest"),
    path("merchants/", merchants, name="merchants"),
    path("hard-declines/export", export_hard_declines),
]