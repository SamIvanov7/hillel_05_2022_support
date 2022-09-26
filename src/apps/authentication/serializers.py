from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    username = serializers.CharField(max_length=50, min_length=4)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "phone", "password", "token"]

    def validate(self, args):

        email = args.get("email", None)
        username = args.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ("username already exists")})

        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "phone", "password", "token")
        read_only_fields = "token"

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
            if password is not None:
                instance.set_password(password)
                instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email adress or mobile phone is required")

        if password is None:
            raise serializers.ValidationError("Password is required")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("User not found")

        if not user.is_active:
            raise serializers.ValidationError("This user is deactivated")

        return {"email": user.email, "username": user.username, "phone": user.phone, "token": user.token}
