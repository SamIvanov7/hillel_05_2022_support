from django.db.models import Q
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config.constants import DEFAULT_ROLES
from core.license import (
    IsAuthenticatedAndNotAdmin,
    IsAuthenticatedAndOwner,
    OperatorOnly,
)
from core.models import Ticket
from core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketPutSerializer,
    TicketSerializer,
)
from core.services import TicketsCRUD


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


class GetTicketsListAPI(CustomAPIView):
    """
    API Endpoint to List Tickets
    METHODS: GET, POST
    Available Query Params (For Admins Only!) :
        tickets?empty=true, # returns all tickets without Operator
        tickets?empty=false, # returns all tickets without Operator + CurrentOperator
    """

    queryset = Ticket.objects.all()
    lookup_field = ("id",)
    lookup_url_kwarg = ("id",)
    permission_classes = {
        "get": [IsAuthenticatedAndOwner],
        "post": [IsAuthenticatedAndNotAdmin],
    }

    def get(self, request):
        user = self.request.user
        if self.request.user.is_staff:
            empty = request.query_params.get("empty", None)
            if empty == "false":
                tickets = Ticket.objects.filter(Q(operator=user) | Q(operator=None))
                serializer = TicketLightSerializer(tickets, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            if empty == "true":
                tickets = Ticket.objects.filter(operator=None)
                ticket_serializer = TicketLightSerializer(tickets, many=True)
                return Response(ticket_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
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
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


class TicketAssignAPI(UpdateAPIView):
    http_method_names = ["patch"]
    serializer_class = TicketAssignSerializer
    permission_classes = [OperatorOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Ticket.objects.filter(operator=None)


class TicketResolveAPI(UpdateAPIView):
    http_method_names = ["patch"]
    permission_classes = [OperatorOnly]
    serializer_class = TicketLightSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(operator=user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = TicketsCRUD.change_resolved_status(instance)

        # serializer = self.serializer_class(instance)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)


# class MyViewSet(viewsets.ModelViewSet):

#     def update(self, request, *args, **kwargs):
#         self.methods=('put',)
#         self.permission_classes = (CustomPermissions)
#         return super(self.__class__, self).update(request, *args, **kwargs)


# @api_view(["GET", "POST", "DELETE"])
# @permission_classes([TicketPermission])
# def get_all_tickets(request):

#     # GET list of tickets, POST new ticket, DELETE all tickets

#     if request.method == "GET":
#         tickets = Ticket.objects.all()
#         # search by themeZ
#         theme = request.query_params.get("theme", None)

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
