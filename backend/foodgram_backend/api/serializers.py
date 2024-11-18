from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe
from foodgram_backend.fields import Base64ImageField



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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра произведений."""

    ingredients = IngredientSerializer(required=False, many=True)
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
        read_only_fields = (
            "author",
        )
