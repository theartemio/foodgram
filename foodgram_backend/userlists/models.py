from django.db import models

from .abstract_models import UserRecipeListsAbstract


class Favorites(UserRecipeListsAbstract):
    """Модель для хранения списка избранных рецептов."""

    class Meta:
        """Проверяет, что рецепт не добавляется в избранное дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_user_recipe_favorite"
            )
        ]


class ShoppingCart(UserRecipeListsAbstract):
    """Модель для хранения рецептов, сохраненных в список покупок."""

    class Meta:
        """Проверяет, что рецепт не добавляется в избранное дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_user_recipe_shopping_cart",
            )
        ]
