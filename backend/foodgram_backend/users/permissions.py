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


class IsAuthOrReadOnly(permissions.BasePermission):
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


class IsSameUserOrRestricted(permissions.BasePermission):
    """Проверяет, что пользователь залогинен и запрашивает записи о себе."""

    def has_permission(self, request, view):
        if request.method == 'GET' and view.action == 'list':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
