from django.db import models
from foodgram_backend.constants import MAX_NAMES_LENGTH, MAX_SLUG_LENGTH

class NameMixin(models.Model):
    """Миксин для простых моделей с двумя полями."""

    name = models.CharField(max_length=MAX_NAMES_LENGTH, verbose_name="Название")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name