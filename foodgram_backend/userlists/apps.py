from django.apps import AppConfig


class UserlistsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userlists'

    def ready(self):
        from . import signals  # noqa
