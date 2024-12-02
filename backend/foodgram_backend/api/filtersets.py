from django.db.models import Exists, OuterRef
from django_filters import rest_framework as filters
from recipes.models import Recipe
from userlists.models import Favorites, ShoppingCart


class RecipeFilter(filters.FilterSet):
    """
    Фильтр для модели Recipe, позволяющий фильтровать добавленные рецепты.
    Фильтрация по полям:
        - is_favorited - выдает рецепты, которые сделавший запрос пользователь
        добавил в избранное.
        - is_in_shopping_cart - пыдает рецепты, которые сделавший запрос
        пользователь добавил в список покупок.
        - tags - фильтрация по тегу через slug, доступна фильтрация по
        множеству тегов, переданных в одном запросе.
        - author - фильтрция по автору через id автора

    """

    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart"
    )
    tags = filters.CharFilter(method="filter_tags", lookup_expr="iexact")

    class Meta:
        model = Recipe
        fields = ("is_favorited", "is_in_shopping_cart", "tags", "author")

    def filter_is_favorited(self, queryset, name, value):
        """
        Фильтрует рецепты в зависимости от того,
        добавлены ли они в избранное.
        """
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset

        return queryset.annotate(
            is_favorited=Exists(
                Favorites.objects.filter(user=user, recipe=OuterRef("pk"))
            )
        ).filter(is_favorited=value)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """
        Фильтрует рецепты в зависимости от того,
        добавлены ли они в список покупок.
        """
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset
        return queryset.annotate(
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(user=user, recipe=OuterRef("pk"))
            )
        ).filter(is_in_shopping_cart=value)

    def filter_tags(self, queryset, name, value):
        """
        Фильтрует рецепты по тегам.
        """
        tags = self.request.query_params.getlist("tags")
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        return queryset
