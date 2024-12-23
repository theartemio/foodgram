from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Recipe


class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра краткой информации
    о рецептах в списке подписок.
    """

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
