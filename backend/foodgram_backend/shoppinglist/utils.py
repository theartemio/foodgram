from .models import UserIngredients


def is_in_list(user, model, object):
    """
    Проверяет, существует ли пара user-recipe в m2m моделях,
    например списках рецептов.

    Принимает аргументы:
        - model - модель, в которой записана связь
        - user - пользователь, которого необходимо проверить
        - obj - объект, с которым должен быть
        связан пользователь.

    В случае анонимных пользователей возвращает False
    """
    if user.is_anonymous:
        return False
    in_list = model.objects.filter(user=user, recipe=object).exists()
    return in_list


def upgrade_ingredient_list(ingredients, user, adding=True):
    """
    Функция для обновления списка ингредиентов.
    Принимает список из словарей, содержащих ингредиенты и их
    количества, юзера и булево значение adding, указывающее на то,
    добавляет ли пользователь рецепт к списку, или удаляет.
    """

    for ingredient in ingredients:
        ingredient_id = ingredient["id"]
        ingredient_amount = (
            ingredient["amount"] if adding else (-ingredient["amount"])
        )
        ingredient_in_list = UserIngredients.objects.filter(
            ingredient_id=ingredient_id
        ).first()
        if ingredient_in_list:
            current_total = ingredient_in_list.total
            updated_total = current_total + ingredient_amount
            if updated_total == 0:
                UserIngredients.objects.get(ingredient_id=ingredient_id).delete()
            else:
                ingredient_in_list.total = updated_total
                ingredient_in_list.save()
        else:
            UserIngredients.objects.create(
                user=user,
                ingredient_id=ingredient_id,
                total=ingredient_amount,
            )
