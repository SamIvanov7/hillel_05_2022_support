from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.api import login_APIView, registration_APIView, update_APIView

router = DefaultRouter()

app_name = "authentication"
urlpatterns = [
    path("update/", update_APIView),
    path("registration/", registration_APIView),
    path("login/", login_APIView),
]
