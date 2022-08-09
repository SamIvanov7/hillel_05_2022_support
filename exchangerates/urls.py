from django.urls import path

from exchangerates.api import btc_usd, history

urlpatterns = [
    path("btc_usd/", btc_usd),
    path("history/", history),
]
