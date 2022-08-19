from django.urls import path

from authentication.api import registrationAPIView

app_name = "authentication"
urlpatterns = [path("users/", registrationAPIView)]
