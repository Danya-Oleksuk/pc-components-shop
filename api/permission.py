from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if not request.user or request.user.is_anonymous:
            return False
        return request.user.is_staff or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if not request.user or request.user.is_anonymous:
            return False
        return request.user.is_staff or request.user.is_superuser


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
