from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class UserRecipeListsAbstract(models.Model):
    """
    Абстрактная модель для создания M2M промежуточных моделей со списками
    рецептов.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=False,
        verbose_name="Рецепт",
        help_text="Id рецепта, к которому относится ингредиент.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
    )

    class Meta:

        abstract = True
