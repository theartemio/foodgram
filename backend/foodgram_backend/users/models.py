from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.db import models

from foodgram_backend.constants import (CHOICES, MAX_EMAIL_LENGTH,
                                        MAX_NAMES_LENGTH, MAX_ROLE_LENGTH,
                                        USER)


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
        upload_to="users/avatars/",
        null=True,
        default=None,
        verbose_name="Аватар",
        help_text="Аватар или, как говорили встарь, юзерпик.",
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
    objects = UserManager()


class Follow(models.Model):
    """
    Модель для хранения подписок пользователей.
    Реализует связь многие-ко-многим.
    Каждая запись связана с моделью User:
        - Поле user - на пользователя, которому принадлежит
        список подписок.
        - Поле following - на пользователя, на которого
        подписан user.
    """

    user = models.ForeignKey(
        CustomUser, related_name="user", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )

    class Meta:
        """Проверяет что подписка не добавляется дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            )
        ]
