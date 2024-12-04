from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram_backend.constants import MAX_NAMES_LENGTH
from foodgram_backend.utils import is_in_list
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from userlists.models import Favorites, ShoppingCart
from users.serializers import CustomUserSerializer

from .serializer_mixins import UserRecipeListsMixin


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

    id = serializers.IntegerField(source="ingredient_id.id")
    amount = serializers.IntegerField()

    class Meta:
        fields = (
            "id",
            "amount",
        )
        model = RecipeIngredient

    def validate_id(self, value):
        """Проверка существования ингредиента."""
        if not Ingredient.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Ингредиент с ID {value} не существует."
            )
        return value

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Количество ингдериента не может быть меньше 1!"
            )
        return value


class RecipeAddingSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов."""

    ingredients = RecipeIngredientSerializer(
        many=True, required=True, allow_empty=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=True, allow_empty=False
    )
    image = Base64ImageField(required=True)
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

    def validate(self, data):
        if not data["image"]:
            raise serializers.ValidationError("Картинка обязательна!")
        return data

    def validate_tags(self, value):
        unique_tags = set(value)
        if len(value) != len(unique_tags):
            raise serializers.ValidationError("Теги не могут повторяться!")
        return value

    def add_ingredients(self, recipe, ingredients_data):
        """Описывает логику добавления ингредиентов к рецепту."""

        recipe_ingredients = []
        added_ingredient_ids = set()
        for ingredient in ingredients_data:
            ingredient_id = ingredient["ingredient_id"]["id"]
            if ingredient_id in added_ingredient_ids:
                raise serializers.ValidationError(
                    f"Ингредиент с ID {ingredient_id} повторяется."
                )
            amount = ingredient["amount"]
            recipe_ingredient = RecipeIngredient(
                recipe=recipe, ingredient_id=ingredient_id, amount=amount
            )
            recipe_ingredients.append(recipe_ingredient)
            added_ingredient_ids.add(ingredient_id)
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта."""
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        self.add_ingredients(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецепта."""
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if ingredients is not None:
            RecipeIngredient.objects.filter(recipe=instance).delete()
            self.add_ingredients(instance, ingredients)
        if tags is not None:
            instance.tags.set(tags)
        instance.save()
        return instance


class RecipeDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального просмотра рецептов.
    Ингредиенты, теги и автор передаются в виде объектов.
    Включает дополнительные поля:
        - is_favorited - поле для проверки того,
        добавлен ли рецепт в список избранного.
        - is_in_shopping_cart - поле для проверки того,
        добавлен ли рецепт в список покупок.
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


class ShoppingCartSerializer(
    UserRecipeListsMixin, serializers.ModelSerializer
):
    """
    Сериализатор для составления списка покупок.
    """

    class Meta:
        fields = (
            "user",
            "recipe",
        )
        model = ShoppingCart
