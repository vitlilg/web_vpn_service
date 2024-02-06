from rest_framework import permissions

from apps.users.models import User


class WebsitePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        request_user = request.user
        if request.method in ['GET', 'POST', 'PUT', 'PATCH']:
            return request_user.is_authenticated and request_user.type_user == User.TypeUserChoices.CUSTOMER
        return False
