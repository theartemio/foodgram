from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from foodgram_backend.utils import get_ingredients_with_amounts

from .models import ShoppingCart
from .utils import upgrade_ingredient_list

User = get_user_model()


@receiver(post_save, sender=ShoppingCart)
def add_to_ingredient_list(sender, instance, created, **kwargs):
    """
    Обновляет модель UserIngredients после
    добавления рецепта в список покупок.
    """
    if created:
        user = instance.user
        recipe_id = instance.recipe.id
        ingredients = get_ingredients_with_amounts(recipe_id)
        if ingredients:
            upgrade_ingredient_list(
                ingredients=ingredients, user=user, adding=True
            )


@receiver(post_delete, sender=ShoppingCart)
def remove_from_ingredient_list(sender, instance, **kwargs):
    """
    Обновляет модель UserIngredients после
    удаления рецепта из списка покупок.
    """
    user = instance.user
    recipe_id = instance.recipe.id
    ingredients = get_ingredients_with_amounts(recipe_id)
    if ingredients:
        upgrade_ingredient_list(
            ingredients=ingredients, user=user, adding=False
        )
