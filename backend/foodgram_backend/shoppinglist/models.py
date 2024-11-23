from django.db import models
from django.contrib.auth import get_user_model

from .abstract_models import UserRecipeListsAbstract
from recipes.models import Ingredient
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from rest_framework import serializers, status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe

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
                fields=["user", "ingredient"], name="unique_user_ingredient_cart"
            )
        ]
