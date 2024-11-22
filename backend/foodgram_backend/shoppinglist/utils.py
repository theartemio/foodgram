def get_image_url(instance):
    """Функция, возвращающая URL картинки."""
    if instance:
        return instance.url
    return None
