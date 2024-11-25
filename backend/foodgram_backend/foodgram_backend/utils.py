from recipes.models import RecipeIngredient


def get_image_url(instance):
    """Функция, возвращающая URL картинки."""
    if instance:
        return instance.url
    return None

def get_ingredients_with_amounts(recipe_id):
    """Возвращает список ингредиентов и их количеств для рецепта с id = recipe_id"""
    recipe_ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    ingredients = []
    for recipe_ingredient in recipe_ingredients:
        ingredient = recipe_ingredient.ingredient
        amount = recipe_ingredient.amount
        ingredients.append({"id": ingredient.id, "amount": amount})
    return ingredients
