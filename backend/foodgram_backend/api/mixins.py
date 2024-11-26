from rest_framework import filters, response, status
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

# from users.permissions import IsAdminOrReadonly, IsAuthOrReadOnly
from foodgram_backend.constants import GET_POST_DELETE, GET


class NoPaginationMixin:
    """Миксин отключения пагинации."""

    pagination_class = None

class SearchMixin:
    """Миксин для настройки поиска по имени."""

    # lookup_field = "slug"  # Фильтр по слагу, не нужен в этом проекте
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class SearchAndFilterMixin:
    """
    Миксин для фильтрации по тегам и
    поиска по:
        - Названию
        - Автору
    """

    # lookup_field = "slug"
    # filter_backends = (filters.SearchFilter,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("is_favorited",
            "is_in_shopping_cart",) 
    # search_fields = ("name",)
    pass
