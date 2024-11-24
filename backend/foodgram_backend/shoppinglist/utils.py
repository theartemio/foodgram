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
    in_list = model.objects.filter(
            user=user, recipe=object
        ).exists()
    return in_list
