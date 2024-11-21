from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer
from rest_framework import serializers
from foodgram_backend.fields import Base64ImageField
from .models import Follow
from recipes.models import Recipe

User = get_user_model()


# Для теста
class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра рецептов."""

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class CustomUserSerializer(UserSerializer):
    """
    Кастомный сериализатор пользователя для
    эндпоинтов /api/users/me/ и /api/users/me/
    """

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
        ]


class SubscriptionUserSerializer(UserSerializer):
    """
    Кастомный сериализатор пользователя для
    просмотра юзера с рецептами
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = RecipeSubscriptionsSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        ]

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        subscribed = Follow.objects.filter(user=user, following=obj).exists()
        return subscribed

    def get_recipes_count(self, obj):
        recipes = obj.recipes
        if recipes:
            return recipes.count()
        return 0


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара, нужен для работы с полем Base64ImageField."""

    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("avatar",)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.ReadOnlyField(source="user.id")
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        """
        Проверяет что:
            - Пользователь не пытается подписаться на самого себя.
            - Пользователь не пытается подписаться на другого пользователя
            повторно.
        """
        user = self.context["request"].user
        if data["following"] == user:
            raise serializers.ValidationError(
                "Зачем вам подписываться на самого себя?!"
            )
        if Follow.objects.filter(
            user=user, following=data["following"]
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора."
            )
        return data

    class Meta:
        fields = (
            "user",
            "following",
        )
        model = Follow
