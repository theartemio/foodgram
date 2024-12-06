from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class NameStartsWithFilter(filters.FilterSet):

    class Meta:
        model = Ingredient
        fields = {
            "name": ["startswith", "exact"],
        }
        search_fields = ("name",)
        filter_overrides = {"name": {"lookup_type": "startswith"}}


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
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

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
        if value:
            return queryset.filter(userlists_favorites_list__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """
        Фильтрует рецепты в зависимости от того,
        добавлены ли они в список покупок.
        """
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset
        if value:
            return queryset.filter(userlists_shoppingcart_list__user=user)
