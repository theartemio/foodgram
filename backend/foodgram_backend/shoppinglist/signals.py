from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import ShoppingCart, UserIngredients
from recipes.models import RecipeIngredient, Recipe
from django.shortcuts import get_object_or_404

User = get_user_model()


def get_ingredients_with_values(recipe_id):
    """Возвращает список ингредиентов и их количеств для рецепта с id = recipe_id"""
    recipe_ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    ingredients = []
    for recipe_ingredient in recipe_ingredients:
        ingredient = recipe_ingredient.ingredient
        value = recipe_ingredient.value
        ingredients.append({"id": ingredient.id, "value": value})
    return ingredients


@receiver(post_save, sender=ShoppingCart)
def update_shopping_cart(sender, instance, created, **kwargs):
    """"""
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
