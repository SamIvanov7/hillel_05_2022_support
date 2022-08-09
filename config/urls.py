from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tickets/", include("core.urls")),
    path("exchangerates/", include("exchangerates.urls")),
]
