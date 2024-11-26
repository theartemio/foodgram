from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Recipe

User = get_user_model()

class UserRecipeListsAbstract(models.Model):
    """
    Абстрактная модель для создания M2M промежуточных моделей со списками
    рецептов без добавления полей к модели User или Recipe.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        related_name="%(app_label)s_%(class)s_list",
        verbose_name="Рецепт",
        help_text="Id рецепта, добавленного в список.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="%(app_label)s_%(class)s_owner",
        verbose_name="Пользователь",
        help_text="Id пользователя, добавившего рецепт в список.",
    )

    class Meta:

        abstract = True
