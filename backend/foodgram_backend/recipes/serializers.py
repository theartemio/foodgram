from .models import Recipe
from foodgram_backend.fields import Base64ImageField
from foodgram_backend.utils import get_image_url
from rest_framework import serializers

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

