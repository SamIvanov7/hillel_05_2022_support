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
        attrs["user"] = self.context["request"].user
        return attrs
