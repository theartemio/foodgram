from rest_framework import filters


class NoPaginationMixin:
    """Миксин отключения пагинации."""

    pagination_class = None


class SearchMixin:
    """Миксин для настройки поиска по названию."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)
