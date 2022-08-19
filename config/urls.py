from django.contrib import admin
from django.urls import include, path

#  from core.api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("authentication.urls", namespace="authentication")),
    path("tickets/", include("core.urls")),
    path("exchangerates/", include("exchangerates.urls")),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
