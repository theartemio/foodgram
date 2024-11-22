from django.db import models
from django.contrib.auth import get_user_model

from .abstract_models import UserRecipeListsAbstract

User = get_user_model()


class Favorites(UserRecipeListsAbstract):
    """Модель для хранения избранных рецептов."""

    class Meta:
        """Проверяет, что рецепт не добавляется в избранное дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe_fave"
            )
        ]


class ShoppingCart(UserRecipeListsAbstract):
    """Модель для хранения рецептов из списка покупок."""

    class Meta:
        """Проверяет, что рецепт не добавляется в избранное дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe_cart"
            )
        ]
