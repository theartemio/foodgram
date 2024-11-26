from rest_framework import serializers

from .serializer_mixins import UserRecipeListsMixin
from .models import Favorites, ShoppingCart


class FavoritesSerializer(UserRecipeListsMixin, serializers.ModelSerializer):
    """
    Сериализатор для составления списка избранного.
    """

    class Meta:
        fields = (
            "user",
            "recipe",
        )
        model = Favorites


class ShoppingCartSerializer(UserRecipeListsMixin, serializers.ModelSerializer):
    """
    Сериализатор для составления списка покупок.
    """

    class Meta:
        fields = (
            "user",
            "recipe",
        )
        model = ShoppingCart
