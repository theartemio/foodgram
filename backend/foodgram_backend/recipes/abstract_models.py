from django.db import models
from foodgram_backend.constants import MAX_NAMES_LENGTH


class NameMixin(models.Model):
    """Миксин для добавления поля name в модель."""

    name = models.CharField(
        max_length=MAX_NAMES_LENGTH, verbose_name="Название"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
