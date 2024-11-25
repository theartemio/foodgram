from rest_framework import filters, response, status
from rest_framework.pagination import LimitOffsetPagination

# from users.permissions import IsAdminOrReadonly, IsAuthOrReadOnly
from foodgram_backend.constants import GET_POST_DELETE


class NoPaginationMixin:
    """Миксин отключения пагинации."""

    pagination_class = None

class PaginationMixin:
    """Миксин для настройки пагинации."""

    pagination_class = LimitOffsetPagination

'''
class AuthorPermissionMixin:
    """Миксин для проверки доступа автора и модера."""

    permission_classes = (IsAuthOrReadOnly,)


class AdminOrReadOnlyMixin:
    """Миксин для проверки админства."""

    permission_classes = (IsAdminOrReadonly,)
'''

class GetMixin:
    """Миксин для ограничения методов."""

    http_method_names = GET_POST_DELETE
    # http_method_names = ("get",)

    def retrieve(self, request, *args, **kwargs):
        return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SearchMixin:
    """Миксин для настройки поиска по имени."""

    # lookup_field = "slug"  # Фильтр по слагу, не нужен в этом проекте
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
