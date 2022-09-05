from django.urls import path

from core.api import GetTicketsList, TicketRetrieveAPI

urlpatterns = [
    path("", GetTicketsList.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
]
