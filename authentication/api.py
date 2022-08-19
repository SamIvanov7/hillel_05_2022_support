from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import RegistrationSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def registrationAPIView(request):
    user_data = request.data.get("user", {})
    serializer_class = RegistrationSerializer

    serializer = serializer_class(data=user_data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
