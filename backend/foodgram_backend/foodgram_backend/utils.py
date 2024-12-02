from recipes.models import RecipeIngredient
from userlists.models import UserIngredients


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
    recipe_ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    ingredients = []
    for recipe_ingredient in recipe_ingredients:
        ingredient = recipe_ingredient.ingredient
        amount = recipe_ingredient.amount
        ingredients.append({"id": ingredient.id, "amount": amount})
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


def upgrade_ingredient_list(ingredients, user, model, adding=True):
    """
    Функция для обновления списка ингредиентов.
    Принимает в качестве параметров:
        - список из словарей, содержащих ингредиенты и их
        количества,
        - юзера
        - модель, в которой хранятся ингредиенты пользователя
        - булево значение adding, указывающее на то,
        добавляет ли пользователь рецепт к списку, или удаляет.
    """

    for ingredient in ingredients:
        ingredient_id = ingredient["id"]
        ingredient_amount = (
            ingredient["amount"] if adding else (-ingredient["amount"])
        )
        ingredient_in_list = model.objects.filter(
            ingredient_id=ingredient_id
        ).first()
        if ingredient_in_list:
            current_total = ingredient_in_list.total
            updated_total = current_total + ingredient_amount
            if updated_total == 0:
                model.objects.get(ingredient_id=ingredient_id).delete()
            else:
                ingredient_in_list.total = updated_total
                ingredient_in_list.save()
        else:
            model.objects.create(
                user=user,
                ingredient_id=ingredient_id,
                total=ingredient_amount,
            )


def form_shopping_list(user):
    """Формирует список покупок для отправки в файле."""
    users_ingredients = UserIngredients.objects.filter(user=user.id)
    ingredient_lines = [
        f"Список покупок пользователя {user}",
    ]
    for ingredient in users_ingredients:
        name = ingredient.ingredient.name
        unit = ingredient.ingredient.measurement_unit
        total = ingredient.total
        line = f"{name}, ({unit}) - {total}"
        ingredient_lines.append(line)
    response_data = "\n".join(ingredient_lines)
    return response_data
