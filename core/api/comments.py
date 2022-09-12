from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from core.custom_generics import CustomAPIView
from core.license import IsAuthenticatedAndOwner
from core.models import Comment
from core.serializers import CommentCreateSerializer, CommentSerializer


class CommentsListAPI(ListAPIView):
    http_method_names = ["get"]
    serializer_class = CommentSerializer
    lookup_field = "ticket_id"
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        ticket_id: int = self.kwargs[self.lookup_field]

        # NOTE: Walrus operator usage
        # if ticket_id := self.kwargs.get(self.lookup_field):
        #     raise ValueError("You can not comment unspecified ticket.")

        return Comment.objects.filter(ticket_id=ticket_id)


class CommentCreateAPI(CustomAPIView):
    http_method_names = ["post"]
    serializer_class = CommentCreateSerializer
    permission_classes = {
        "post": [IsAuthenticatedAndOwner],
    }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer.data
            data["id"] = obj.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
