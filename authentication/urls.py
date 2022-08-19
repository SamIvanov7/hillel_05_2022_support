from django.urls import path
from rest_framework.routers import DefaultRouter

from authentication.api import login_APIView, registration_APIView, update_APIView

router = DefaultRouter()

app_name = "authentication"
urlpatterns = [path("user", update_APIView), path("users/", registration_APIView), path("users/login/", login_APIView)]
