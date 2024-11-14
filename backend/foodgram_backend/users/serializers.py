from django.shortcuts import render
from rest_framework import serializers
from django.http import Http404

from django.contrib.auth import get_user_model, password_validation

from .mixins import ValidateUsernameMixin, ValidatePasswordMixin

from .constants import MAX_EMAIL_LENGTH, MAX_NAMES_LENGTH

from django.core.exceptions import ValidationError


User = get_user_model()


class RegistrationSerializer(ValidatePasswordMixin,
    ValidateUsernameMixin, serializers.ModelSerializer
):
    """Сериализация данных при регистрации юзера."""

    email = serializers.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        required=True,
    )
    username = serializers.CharField(
        max_length=MAX_NAMES_LENGTH,
        required=True,
    )
    first_name = serializers.CharField(
        max_length=MAX_NAMES_LENGTH,
        required=True,
    )
    last_name = serializers.CharField(
        max_length=MAX_NAMES_LENGTH,
        required=True,
    )
    password = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "id",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("password", None)
        return representation




class EmailPassTokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения токена с помощью пары Эмейл + Пароль."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
        return {"user": user}


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Сериализация данных при смене пароля."""

    new_password = serializers.CharField(
        required=True,
    )
    current_password = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "new_password",
            "current_password",
        ]

    def validate(self, data):
        if data["new_password"] == data["current_password"]:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Новый пароль не должен быть старым паролем!"
                    )
                }
            )
        print(self.context)
        request = self.context["request"]
        user = request.user
        errors = []

        # этот кусочек я хочу вынести в utils.py и потом использовать тут и в миксине
        try:
            password_validation.validate_password(password=data["new_password"])
        except ValidationError as error:
            errors = list(error.messages)
        if errors:
            raise serializers.ValidationError({
                "new_password":errors
            })
        return data





# Тест, переписать чтобы можн было делать PATCH
class UsersMeSerializer(ValidateUsernameMixin, serializers.ModelSerializer):

    first_name = serializers.CharField(
        max_length=MAX_EMAIL_LENGTH, required=False
    )
    last_name = serializers.CharField(
        max_length=MAX_NAMES_LENGTH, required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
