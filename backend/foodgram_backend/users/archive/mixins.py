import re

from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation

from ..constants import USERNAME_PATTERN
from django.core.exceptions import ValidationError


class ValidateUsernameMixin:
    """Миксин для валидации юзернейма по паттерну."""

    def validate_username(self, value):
        """
        Проверяет юзернейм по паттерну, а также не дает использовать
        юзернейм me.
        """
        if value == "me":
            error_message = "Юзернейм не может быть 'me'!"
            raise serializers.ValidationError(error_message)
        if not re.fullmatch(USERNAME_PATTERN, value):
            error_message = "Юзернейм содержит недопустимые символы!"
            raise serializers.ValidationError(error_message)
        return value


class ValidatePasswordMixin:
    """Миксин для валидации пароля."""

    def validate_password(self, value):
        errors = []
        try:
            password_validation.validate_password(password=value)
        except ValidationError as error:
            errors = list(error.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return value
