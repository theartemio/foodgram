from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer
from rest_framework import serializers
from foodgram_backend.fields import Base64ImageField
from .models import Follow

User = get_user_model()


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


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватара, нужен для работы с полем Base64ImageField."""

    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("avatar",)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = serializers.ReadOnlyField(source="user.username")
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

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
