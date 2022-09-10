from django.urls import path, re_path

from core.api import (
    GetTicketsListAPI,
    TicketAssignAPI,
    TicketResolveAPI,
    TicketRetrieveAPI,
)

urlpatterns = [
    re_path(r"", GetTicketsListAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
    path("<int:id>/resolve/", TicketResolveAPI.as_view()),
]
