# from rest_framework import serializers, status
# from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from authentication.license import IsOwnerProfileOrReadOnly
# from authentication.models import User
# from authentication.serializers import RegistrationSerializer, UserSerializer


# class UserDetailApiView(RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsOwnerProfileOrReadOnly]


# class RegistrationAPIView(APIView):
#     permission_classes = AllowAny
#     serializer_class = RegistrationSerializer

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"Message": "User created succesfully", "User": serializer.data},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response({"Errors": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)


# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = IsAuthenticated
#     serializer_class = UserSerializer

#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.serializer_class(request.user)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):

#         serializer_data = request.data.get("user", {})
#         serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class LoginAPIView(APIView):
#     permission_classes = AllowAny
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data.get("user", {})
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# class UserListCreateApiView(ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [IsAuthenticated]

#    def perform_create(self, serializer):
#      user = self.request.user
#      serializer.save(user=user)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def registration_APIView(request):

#     serializer_class = RegistrationSerializer
#     user_data = request.data.get("user", {})

#     serializer = serializer_class(data=user_data)
#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_APIView(request):

#     serializer_class = LoginSerializer
#     user = request.data.get("user", {})
#     serializer = serializer_class(data=user)
#     serializer.is_valid(raise_exception=True)

#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["PUT"])
# def update_APIView(self, request, *args, **kwargs):

#     serializer_class = UserSerializer
#     serializer_data = request.data.get("user", {})
#     serializer = serializer_class(request.user, data=serializer_data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()

#     return Response(serializer.data, status=status.HTTP_200_OK)
