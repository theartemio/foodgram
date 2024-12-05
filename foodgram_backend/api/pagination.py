from rest_framework.pagination import PageNumberPagination


class RecipesPageNumberPageSizePagination(PageNumberPagination):
    """Пагинация в соответствии с параметрами."""

    page_size_query_param = "page_size"
