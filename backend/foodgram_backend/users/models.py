from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.models import PermissionsMixin

from django.db import models

from .constants import (
    MAX_EMAIL_LENGTH,
    MAX_NAMES_LENGTH,
    MAX_ROLE_LENGTH,
    CHOICES,
    USERNAME_PATTERN,
    USER,
)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name="Эмейл",
        help_text="Эмейл для входа и получения писем",
    )
    username = models.CharField(
        max_length=MAX_NAMES_LENGTH,
        unique=True,
        verbose_name="Юзернейм",
        help_text="Уникальный юзернейм (никнейм, псевдоним).",
    )
    first_name = models.CharField(
        max_length=MAX_NAMES_LENGTH,
        verbose_name="Имя",
        help_text="Имя. Полное или ваше любимое сокращение, например 'Васёк'.",
    )
    last_name = models.CharField(
        max_length=MAX_NAMES_LENGTH,
        verbose_name="Фамилия",
        help_text="Фамилия. Настоящая или выдуманная.",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, default=None
    )
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=CHOICES,
        default=USER,
        verbose_name="Пользовательская роль.",
        help_text=(
            "Пользователь может быть либо",
            " обычным юзером, либо админом.",
        ),
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
