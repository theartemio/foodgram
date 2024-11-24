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

class IsAdminOrReadonly(permissions.BasePermission):
    """
    Пермишен для админа, обеспечивает доступ для
    изменения только админу, остальным ролям и анонимным
    пользователям доступен просмотр
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == ADMIN
        )


class IsSameUserOrRestricted(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и запрашивает записи о себе."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
        )

class IsSameUserOrReadOnly(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и он - автор записи."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.user == request.user
        )


class IsSameUserOrRestricted(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и запрашивает записи о себе."""

    def has_permission(self, request, view):
        if request.method == "GET" and view.action == "list":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
