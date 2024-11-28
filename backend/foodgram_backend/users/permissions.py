from rest_framework import permissions

from foodgram_backend.constants import ADMIN


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и он - автор записи."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsSameUserOrAdmin(permissions.BasePermission):
    """
    Проверяет, что пользователь запрашивает записи
    о себе или является админом.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.user.role == ADMIN
        )


class IsSameUserOrRestricted(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и запрашивает записи о себе."""

    def has_permission(self, request, view):
        if request.method == "GET" and view.action == "list":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
