from django.core.exceptions import ValidationError
from rest_framework import request, serializers

from apps.core.models import Comment, Ticket


class CommentSerializer(serializers.ModelSerializer):
    # ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # prev_comment = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["ticket", "user", "prev_comment"]

    def validate(self, attrs: dict):
        ticket_id: int = self.context["request"].parser_context["kwargs"]["ticket_id"]
        ticket: Ticket = Ticket.objects.get(id=ticket_id)

        if ticket.operator is None:
            raise ValidationError("Cannot make comment for ticket without operator")
        if not ticket.resolved:
            raise ValidationError("Cannot make comment for resolved ticket")

        attrs["ticket"] = ticket
        attrs["user"] = request.user
        attrs["prev_comment"] = ticket.comments.last()

        return attrs

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)
        return instance
