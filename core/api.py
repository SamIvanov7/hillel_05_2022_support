from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.license import IsAuthenticatedAndNotAdmin, IsAuthenticatedAndOwner
from core.models import Ticket
from core.serializers import (
    TicketLightSerializer,
    TicketPutSerializer,
    TicketSerializer,
)


class CustomAPIView(APIView):
    def get_permissions(self):
        # Instances and returns the dict of permissions that the view requires.
        return {
            key: [permission() for permission in permissions] for key, permissions in self.permission_classes.items()
        }

    def check_permissions(self, request):
        # Gets the request method and the permissions dict, and checks the permissions defined in the key matching
        # the method.
        method = request.method.lower()
        for permission in self.get_permissions()[method]:
            if not permission.has_permission(request, self):
                self.permission_denied(request, message=getattr(permission, "message", None))


class GetTicketsList(CustomAPIView):
    """
    API Endpoint to List Tickets
    METHODS: GET, POST
    """

    permission_classes = {
        "get": [IsAuthenticatedAndOwner],
        "post": [IsAuthenticatedAndNotAdmin],
    }

    def get(self, request):
        user = self.request.user
        if self.request.user.is_staff:
            tickets = Ticket.objects.filter(Q(operator=None) | Q(operator=user))
            serializer = TicketLightSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            tickets = Ticket.objects.filter(client=user)
            serializer = TicketLightSerializer(tickets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TicketPutSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer.data
            data["id"] = obj.id
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TicketRetrieveAPI(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(client=self.request.user)


# class TicketPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "GET":
#             return True
#         return bool(request.user and request.user.is_authenticated)


# class MyViewSet(viewsets.ModelViewSet):

#     def update(self, request, *args, **kwargs):
#         self.methods=('put',)
#         self.permission_classes = (CustomPermissions)
#         return super(self.__class__, self).update(request, *args, **kwargs)


# class GetAndCreateTickets(ListAPIView, CreateAPIView, IsAuthenticatedAndOwner):
#     permission_classes = [IsAuthenticatedAndOwner]
#     def get(self, request, format=None):
#         queryset = Ticket.objects.all()
#         serializer = TicketLightSerializer(queryset, many=True).data
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer =TicketLightSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET", "POST", "DELETE"])
# @permission_classes([TicketPermission])
# def get_all_tickets(request):

#     # GET list of tickets, POST new ticket, DELETE all tickets

#     if request.method == "GET":
#         tickets = Ticket.objects.all()
#         # search by themeZ
#         theme = request.query_params.get("theme", None)
#         if theme is not None:
#             tickets = tickets.filter(theme__icontains=theme)

#         ticket_serializer = TicketLightSerializer(tickets, many=True).data
#         return Response(data=ticket_serializer)

#     # Create ticket
#     elif request.method == "POST":
#         ticket_data = JSONParser().parse(request)
#         ticket_serializer = TicketLightSerializer(data=ticket_data)
#         if ticket_serializer.is_valid():
#             ticket_serializer.save()
#             return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Delete all tickets
#     elif request.method == "DELETE":
#         ticket_count = Ticket.objects.all().delete()
#         return Response(
#             {"message": "{} Tickets were deleted successfully!".format(ticket_count[0])},
#             status=status.HTTP_204_NO_CONTENT,
#         )


# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([TicketPermission])
# def get_ticket(request, id_: int):

#     # Search ticket by id
#     # GET / PUT / DELETE ticket

#     try:
#         ticket = Ticket.objects.get(id=id_)
#     except Ticket.DoesNotExist:
#         return Response({"message": "The ticket does not exist"}, status=status.HTTP_404_NOT_FOUND)

#     # Get ticket
#     if request.method == "GET":
#         ticket_serializer = TicketSerializer(ticket)
#         return Response(ticket_serializer.data)
#     # Update ticket's theme & description
#     if request.method == "PUT":
#         ticket_serializer = TicketPutSerializer(ticket, data=request.data)
#         if ticket_serializer.is_valid():
#             ticket_serializer.save()
#             return Response(ticket_serializer.data)
#         return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # Delete ticket
#     elif request.method == "DELETE":
#         ticket.delete()
#         return Response({"message": "Ticket was deleted succefully"}, status=status.HTTP_204_NO_CONTENT)

# def search(id_):
#     raise TicketNotFound()

# def search_ticket(id_:int) -> Ticket:
#     search(id_)
#     for ticket in tickets:
#         if ticket.id_== id_
#     return ticket
#     raise TicketNotFound
# def get_ticket(self, request, id_: int, format=None):
#     try:
#         tickets = Ticket.objects.get(id=id_)
#     except: Ticket.DoesNotExist: Response({"message": "The ticket does not exist"}, status=status.HTTP_404_NOT_FOUND)
