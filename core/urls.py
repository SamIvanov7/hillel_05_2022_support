from django.urls import path

from core.api.comments import CommentCreateAPI, CommentsListAPI
from core.api.tickets import GetTicketsListAPI, TicketAssignAPI, TicketResolveAPI, TicketRetrieveAPI

tickets_urls = [
    path(r"", GetTicketsListAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
    path("<int:id>/resolve/", TicketResolveAPI.as_view()),
]

comments_urls = [
    path("<int:ticket_id>/comments/", CommentsListAPI.as_view()),
    path("<int:ticket_id>/comments/create/", CommentCreateAPI.as_view()),
]

urlpatterns = tickets_urls + comments_urls
