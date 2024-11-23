from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from foodgram_backend.fields import Base64ImageField
from users.serializers import CustomUserSerializer
from shoppinglist.models import Favorites, ShoppingCart

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        fields = (
            "id",
            "name",
            "slug",
        )
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        fields = (
            "id",
            "name",
            "measure_unit",
        )
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        fields = (
            "id",
            "value",
        )
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра рецептов."""

    ingredients = serializers.ListField(required=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        allow_null=False,
        allow_empty=True,
    )
    image = Base64ImageField(required=False, allow_null=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "author",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра рецептов."""

    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        """Проверяет, в избранном ли рецепт."""
        user = self.context["request"].user
        faved = Favorites.objects.filter(user=user, recipe=obj).exists()
        return faved

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, в списке покупок ли рецепт."""
        user = self.context["request"].user
        in_shopping_cart = ShoppingCart.objects.filter(
            user=user, recipe=obj
        ).exists()
        return in_shopping_cart
