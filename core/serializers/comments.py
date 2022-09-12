from rest_framework import serializers

from core.models import Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        ticket_id: int = request.parser_context["kwargs"]["ticket_id"]
        ticket: Ticket = ticket.objects.get(id=ticket_id)
        attrs["ticket"] = ticket
        attrs["user"] = request.user
        return attrs

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)
        return instance
