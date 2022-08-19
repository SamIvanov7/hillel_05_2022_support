from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def registration_APIView(request):

    serializer_class = RegistrationSerializer
    user_data = request.data.get("user", {})

    serializer = serializer_class(data=user_data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_APIView(request):

    serializer_class = LoginSerializer
    user = request.data.get("user", {})
    serializer = serializer_class(data=user)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_APIView(self, request, *args, **kwargs):

    serializer_class = UserSerializer
    serializer_data = request.data.get("user", {})
    serializer = serializer_class(request.user, data=serializer_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
