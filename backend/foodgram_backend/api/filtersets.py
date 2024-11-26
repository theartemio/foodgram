from django_filters import rest_framework as filters
from recipes.models import Recipe


class TitleFilter(filters.FilterSet):
    """
    Фильтр для модели Recipe, позволяющий фильтровать
    по жанру, категории, году и имени
    """

    is_favorited = filters.CharFilter(field_name="genre__slug", lookup_expr="exact")
    is_in_shopping_cart = filters.CharFilter(
        field_name="category__slug", lookup_expr="exact"
    )
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Recipe
        fields = (
            "genre",
            "category",
            "year",
            "name",
        )
