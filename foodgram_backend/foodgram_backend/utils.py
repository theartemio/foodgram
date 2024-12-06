from recipes.models import RecipeIngredient
from userlists.models import ShoppingCart


def get_image_url(instance):
    """Функция, возвращающая URL картинки."""
    if instance:
        return instance.url
    return None


def get_ingredients_with_amounts(recipe_id):
    """
    Возвращает список связанных с рецептом ингредиентов
    и их количеств.
    Принимает id рецепта.
    """
    recipe_ingredients = RecipeIngredient.objects.filter(
        recipe_id=recipe_id
    ).values("ingredient__id", "amount")
    ingredients = list(recipe_ingredients)
    return ingredients


def is_in_list(user, model, object):
    """
    Проверяет, существует ли пара user-recipe в m2m моделях,
    например списках рецептов.

    Принимает аргументы:
        - model - модель, в которой записана связь
        - user - пользователь, которого необходимо проверить
        - obj - объект, с которым должен быть
        связан пользователь.

    В случае анонимных пользователей возвращает False.
    """
    if user.is_anonymous:
        return False
    in_list = model.objects.filter(user=user, recipe=object).exists()
    return in_list


def form_calculated_cart(user):
    """Формирует список ингредиентов из списка покупок пользователя."""
    calculated_cart = {}
    recipes_in_cart = ShoppingCart.objects.filter(user=user).values_list(
        "recipe", flat=True
    )
    recipe_ingredients = RecipeIngredient.objects.filter(
        recipe__in=recipes_in_cart
    ).select_related("ingredient")
    for recipe_ingredient in recipe_ingredients:
        ingredient = recipe_ingredient.ingredient
        amount = recipe_ingredient.amount
        name = ingredient.name
        if name in calculated_cart.keys():
            calculated_cart[name]["total"] += amount
        else:
            calculated_cart[name] = {
                "total": amount,
                "unit": ingredient.measurement_unit,
            }
    return calculated_cart


def generate_list(shopping_cart, user=""):
    """Формирует список покупок для отправки в файле."""
    ingredient_lines = [
        f"Список покупок пользователя {user}",
    ]
    for ingredient_name in shopping_cart.keys():
        unit = shopping_cart[ingredient_name]["unit"]
        total = shopping_cart[ingredient_name]["total"]
        line = f"{ingredient_name}, ({unit}) - {total}"
        ingredient_lines.append(line)
    response_data = "\n".join(ingredient_lines)
    return response_data
