from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import (
    TicketLightSerializer,
    TicketPutSerializer,
    TicketSerializer,
)


class TicketPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return bool(request.user and request.user.is_authenticated)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([TicketPermission])
def get_all_tickets(request):

    # GET list of tickets, POST new ticket, DELETE all tickets

    if request.method == "GET":
        tickets = Ticket.objects.all()
        # search by themeZ
        theme = request.query_params.get("theme", None)
        if theme is not None:
            tickets = tickets.filter(theme__icontains=theme)

        ticket_serializer = TicketLightSerializer(tickets, many=True).data
        return Response(data=ticket_serializer)

    # Create ticket
    elif request.method == "POST":
        ticket_data = JSONParser().parse(request)
        ticket_serializer = TicketLightSerializer(data=ticket_data)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete all tickets
    elif request.method == "DELETE":
        ticket_count = Ticket.objects.all().delete()
        return Response(
            {"message": "{} Tickets were deleted successfully!".format(ticket_count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([TicketPermission])
def get_ticket(request, id_: int):

    # Search ticket by id
    # GET / PUT / DELETE ticket

    try:
        ticket = Ticket.objects.get(id=id_)
    except Ticket.DoesNotExist:
        return Response({"message": "The ticket does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Get ticket
    if request.method == "GET":
        ticket_serializer = TicketSerializer(ticket)
        return Response(ticket_serializer.data)
    # Update ticket's theme & description
    if request.method == "PUT":
        ticket_serializer = TicketPutSerializer(ticket, data=request.data)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return Response(ticket_serializer.data)
        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete ticket
    elif request.method == "DELETE":
        ticket.delete()
        return Response({"message": "Ticket was deleted succefully"}, status=status.HTTP_204_NO_CONTENT)
