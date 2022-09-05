from django.core.exceptions import ValidationError
from rest_framework import permissions


class IsAuthenticatedAndOwner(permissions.BasePermission):
    message = "You must be admin or authenticated."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthenticatedAndNotAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff and request.method == "POST":
            raise ValidationError({"message": ("admin has not permissions to post tickets")})
        return request.user and request.user.is_authenticated
