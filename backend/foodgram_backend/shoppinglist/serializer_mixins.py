from django.contrib.auth import get_user_model
from foodgram_backend.utils import get_image_url
from recipes.models import Recipe
from rest_framework import serializers

User = get_user_model()


class UserRecipeListsMixin:
    """
    Миксин для сериализаторов для описывающих списки рецептов моделей,
    таких как избранное или список покупок.
    Связан с моделями:
        - User
        - Recipe
    Проверяет, не добавляет ли пользователь рецепт в список повторно.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    
    def validate(self, data):
        """
        Проверяет что:
            - Пользователь не пытается добавить рецепт в список
            повторно.
        """
        model = self.Meta.model
        user = data["user"]
        if model.objects.filter(user=user, recipe=data["recipe"]).exists():
            raise serializers.ValidationError("Рецепт уже добавлен")
        return data

    def to_representation(self, instance):
        """
        Возвращает добавленный рецепт по нужной форме.
        """
        recipe = instance.recipe
        image_url = get_image_url(recipe.image)
        data = {
            "id": recipe.id,
            "name": recipe.name,
            "image": image_url,
            "cooking_time": recipe.cooking_time,
        }
        return data
