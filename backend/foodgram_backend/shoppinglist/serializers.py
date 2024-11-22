
from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer
from rest_framework import serializers
from foodgram_backend.fields import Base64ImageField
from .models import Favorites, ShoppingCart
from recipes.models import Recipe
from .utils import get_image_url
from .mixins import UserRecipeListsMixin


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
