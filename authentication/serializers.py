from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email adress is required")

        if password is None:
            raise serializers.ValidationError("Password is required")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("User not found")

        if not user.is_active:
            raise serializers.ValidationError("This user is deactivated")

        return {"email": user.email, "username": user.username, "token": user.token}


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username,", "password", "token")
        read_only_fields = "token"

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
