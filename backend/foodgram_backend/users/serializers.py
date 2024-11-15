from django.contrib.auth import get_user_model

from djoser.serializers import UserSerializer
from rest_framework import serializers
from .fields import Base64ImageField

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
