from django.urls import path

from apps.exchangerates.api import btc_usd, history

urlpatterns = [
    path("btc_usd/", btc_usd),
    path("history/", history),
]
