from rest_framework import permissions


class IsSameUserOrRestricted(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и запрашивает записи о себе."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
        )
