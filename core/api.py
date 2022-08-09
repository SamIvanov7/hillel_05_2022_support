from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import Role
from core.models import Ticket

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ["created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "username" "email",
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
        fields = ["id", "theme", "description", "operator", "client", "resolved", "created_at", "updated_at"]


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "theme", "resolved", "operator", "client"]


@api_view(["GET"])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    data = TicketLightSerializer(tickets, many=True).data
    return Response(data=data)


@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    return Response(data=data)
