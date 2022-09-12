from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text", "ticket"]

    def validate(self, attrs: dict) -> dict:
        request = self.context["request"]
        attrs["ticket"] = request.parser_context["kwargs"]["ticket_id"]
        attrs["user"] = request.user
        return attrs
