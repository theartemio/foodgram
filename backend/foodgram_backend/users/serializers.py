from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from foodgram_backend.utils import get_image_url
from recipes.serializers import RecipeSubscriptionsSerializer
from rest_framework import serializers

from .mixins import ValidateUsernameMixin
from .models import Follow

User = get_user_model()


class CustomUserCreateSerializer(ValidateUsernameMixin, UserCreateSerializer):
    """
    Кастомный сериализатор для регистрации пользователя с проверкой юзернейма.
    """

    pass


class CustomUserSerializer(ValidateUsernameMixin, UserSerializer):
    """
    Сериализатор пользователя просмотра пользователя
    в сокращенном виде, без списка рецептов и их счетчика.
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        ]

    def get_is_subscribed(self, obj):
        """
        Проверяет подписку. В случае анонимного
        пользователя возвращает False.
        """

        user = self.context["request"].user
        if user.is_anonymous:
            return False
        subscribed = Follow.objects.filter(user=user, following=obj).exists()
        return subscribed


class SubscriptionsUsersSerializer(UserSerializer):
    """
    Сериализатор для просмотра детальной информации о юзере
    со списком рецептов, их счетчиком и данными о подписке.
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
        """Проверяет подписку."""
        user = self.context["request"].user
        subscribed = Follow.objects.filter(user=user, following=obj).exists()
        return subscribed

    def to_representation(self, instance):
        """Возвращает количество рецептов в соответствии с recipes_limit"""
        data = super(SubscriptionsUsersSerializer, self).to_representation(
            instance
        )
        request = self.context["request"]
        limit = request.query_params.get("recipes_limit")
        if limit:
            recipes = data.pop("recipes")
            limited_recipes = recipes[: int(limit)]
            data["recipes"] = limited_recipes
        return data

    def get_recipes_count(self, obj):
        """Считает рецепты."""
        recipes = obj.recipes
        if recipes:
            return recipes.count()
        return 0


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для загрузки аватара, позволяет загрузить картинку
    через поле Base64ImageField.
    """

    avatar = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = User
        fields = ("avatar",)

    def to_representation(self, instance):
        """
        Возвращает ссылку на аватар.
        """

        user = self.context["user"]
        image_url = get_image_url(user.avatar)
        data = {
            "avatar": image_url,
        }
        return data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления подписки в модель Follow."""

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
            err_message = (
                "Мы любим чревоугодие, а не тщеславие.",
                "Не подписывайтесь на самого себя!",
            )
            raise serializers.ValidationError(err_message)
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
