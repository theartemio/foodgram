from django.contrib.auth import get_user_model

from recipes.models import Recipe
from rest_framework import serializers

from foodgram_backend.fields import Base64ImageField


User = get_user_model()

class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра краткой информации о рецептах в списке подписок."""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )