from rest_framework import permissions


class IsAdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.type_user == user.TypeUserChoices.ADMIN
