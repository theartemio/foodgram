from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ToBuy(models.Model):
    """
    Модель для хранения списков покупок пользователей.
    Реализует связь многие-ко-многим и количество продукта.
    Каждая запись связана с моделью User:
        - Поле user - на пользователя, которому принадлежит
        список подписок.
        - Поле following - на пользователя, на которого
        подписан user.
    """

    user = models.ForeignKey(
        User, related_name="shopping_user", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        User, related_name="ingredient", on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Время приготовления в минутах.",
    )

    class Meta:
        """Проверяет, что ингредиент не добавляется дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "ingredient"], name="unique_ingredients"
            )
        ]

    def __str__(self):
        return f"follows"
