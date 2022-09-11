from itertools import chain

from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.models import Role
from core.models import Ticket

User = get_user_model()


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

    def validate(self, attrs: dict) -> dict:
        theme = attrs.get("theme")

        if not theme:
            return attrs

        data = Ticket.objects.value("theme")

        for element in chain.from_iterable(data):
            if element == theme:
                raise ValueError("This ticket is already in database")

        return attrs


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


class TicketPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "theme",
            "description",
        ]

    def validate(self, attrs: dict) -> dict:
        theme = attrs.get("theme")

        if not theme:
            return attrs

        data = Ticket.objects.values_list("theme")

        for element in chain.from_iterable(data):
            if element == theme:
                raise ValueError("This ticket is already in database")
        return attrs

    def new_method(self, attrs):
        attrs["client"] = self.context["request"].user


class TicketAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["operator"]

    def validate(self, attrs: dict) -> dict:
        # NOTE: Add current user to the `attrs` object
        attrs["operator"] = self.context["request"].user
