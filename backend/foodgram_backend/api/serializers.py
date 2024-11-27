from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from shoppinglist.models import Favorites, ShoppingCart
from foodgram_backend.utils import is_in_list
from users.serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404

from foodgram_backend.fields import Base64ImageField
from django.http import Http404

from foodgram_backend.constants import MAX_NAMES_LENGTH

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
            "measurement_unit",
        )
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RecipeIngredient,
    позволяет добавлять ингредиенты и их количества
    к рецепту.
    """

    # id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = (
            "id",
            "amount",
        )
        model = RecipeIngredient


class RecipeAddingSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов."""

    ingredients = serializers.ListField(required=True)
    # ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
        allow_null=False,
        allow_empty=False,
    )
    image = Base64ImageField(required=True, allow_null=True)
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    name = serializers.CharField(required=True, max_length=MAX_NAMES_LENGTH)
    text = serializers.CharField(required=True)

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

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "Список ингредиентов не может быть пустым!"
            )
        keys = []
        for ingredient in value:
            id = ingredient["id"]
            try:
                ingredient = Ingredient.objects.get(id=id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError("Ингредиент не найден!")
            keys.append(id)
        if len(keys) != len(set(keys)):
            raise serializers.ValidationError(
                "Ингредиенты не могут повторяться!"
            )
        return value

    def validate_tags(self, value):
        unique_tags = set(value)
        if len(value) != len(unique_tags):
            raise serializers.ValidationError("Теги не могут повторяться!")
        return value


class RecipeDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального просмотра рецептов.
    Ингредиенты, теги и автор передаются в виде объектов.
    Включает дополнительные поля:
        - is_favorited - поле для проверки того,
        добавлен ли рецепт в список избранного
        - is_in_shopping_cart - поле для проверки того,
        добавлен ли рецепт в список покупок
    """

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
        is_faved = is_in_list(
            model=Favorites, user=self.context["request"].user, object=obj
        )
        return is_faved

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, в списке покупок ли рецепт."""
        in_shopping_cart = is_in_list(
            model=ShoppingCart,
            user=self.context["request"].user,
            object=obj,
        )
        return in_shopping_cart

    def to_representation(self, instance):
        """Добавляет к списку ингредиентов количества."""
        data = super(RecipeDetailSerializer, self).to_representation(instance)
        ingredients = data["ingredients"]
        recipe_id = data["id"]
        for ingredient in ingredients:
            amount = RecipeIngredient.objects.get(
                ingredient_id=ingredient["id"], recipe_id=recipe_id
            ).amount
            ingredient["amount"] = amount
        data.update({"ingredients": ingredients})
        return data
