from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponse
import datetime

from authentication.models import Role
from core.models import Ticket

User = get_user_model()

def user_as_dict(user: User) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.phone,
        "last_name": user.phone,
        "age": user.phone,
    }


def ticket_as_dict(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,  # type: ignore
        "theme": ticket.theme,
        "description": ticket.description,
        "operator": user_as_dict(ticket.operator),
        "resolved": ticket.resolved,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
    }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = [
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "first_name",
            "last_name",
            "age",
            "phone",
        ]


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer()
    client = UserSerializer()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "theme",
            "description",
            "operator",
            "client",
            "resolved",
            "created_at",
            "updated_at",
        ]


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "theme",
            "resolved",
            "operator",
            "client",
        ]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer(queryset, many=True).data
    

@api_view(["GET"])
def get_all_tickets(request):
    result = TicketViewSet.serializer_class
    return Response(data=result)

@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    result = TicketSerializer(tickets).data
    return Response(data=result)

