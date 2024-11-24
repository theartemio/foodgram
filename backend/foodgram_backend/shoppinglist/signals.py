from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from foodgram_backend.utils import get_ingredients_with_values

from .models import ShoppingCart, UserIngredients

User = get_user_model()

@receiver(post_save, sender=ShoppingCart)
def update_shopping_cart(sender, instance, created, **kwargs):
    """Обновляет модель UserIngredients после добавления рецептов в список покупок."""
    if created:
        user = instance.user
        recipe_id = instance.recipe.id
        ingredients = get_ingredients_with_values(recipe_id)
        if ingredients:
            for ingredient in ingredients:
                ingredient_id = ingredient["id"]
                value = ingredient["value"]
                ingredient_in_list = UserIngredients.objects.filter(
                    ingredient_id=ingredient_id
                ).first()  # Не нравится, переписать
                if ingredient_in_list:
                    current_total = ingredient_in_list.total
                    new_total = current_total + value
                    ingredient_in_list.total = new_total
                    ingredient_in_list.save()
                else:
                    UserIngredients.objects.create(
                        user=user,
                        ingredient_id=ingredient_id,
                        total=value,
                    )
