from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Ingredient

from .abstract_models import UserRecipeListsAbstract

User = get_user_model()


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


class UserIngredients(models.Model):
    """
    Модель для хранения ингредиентов пользователя.
    Модель обновляется каждый раз при добавлении рецепта в список
    покупок, обновление осущестляет сигнал update_shopping_cart.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=False,
    )
    total = models.PositiveSmallIntegerField()

    class Meta:
        """Проверяет, что рецепт не добавляется в избранное дважды."""

        constraints = [
            models.UniqueConstraint(
                fields=["user", "ingredient"],
                name="unique_user_ingredient_shopping_cart",
            )
        ]
