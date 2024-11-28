import random
import string

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram_backend.constants import (MAX_NAMES_LENGTH, MAX_SHORT_LINK_CODE,
                                        MAX_SLUG_LENGTH)

from .abstract_models import NameMixin

User = get_user_model()


class Tag(NameMixin, models.Model):
    """Модель для хранения тегов."""

    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        verbose_name="Слаг",
        help_text=(
            "Уникальный слаг, по которому можно указать тег",
            "Рекомендуется использовать понятный слаг,",
            " например транслитерацию или английское название.",
        ),
    )


class Ingredient(NameMixin, models.Model):
    """Модель для хранения ингредиентов."""

    measurement_unit = models.CharField(
        max_length=MAX_NAMES_LENGTH,
        verbose_name="Единица измерения",
        help_text=(
            "Единица измерения, которую можно использовать",
            " для ингредиента. Рекомендуется писать целиком",
            " или использовать понятное сокращение.",
        ),
    )


class Recipe(models.Model):
    """
    Модель для хранения рецептов.
    Модель связана с моделями Tag, Ingredient, User:
        - Поле tag (необязательное) связано с моделью Tag,
        у одного рецепта допускается несколько тегов,
        переданных списком.
        - Поле ingredient, связано с моделью Ingredient
        У одного рецепта допускается несколько ингредиентов,
        переданных списком.
        - Поле author (обязательное, заполняется автоматически)
        связано с моделью User.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        help_text="Автор рецепта. Присваивается автоматически.",
    )
    name = models.CharField(
        max_length=MAX_NAMES_LENGTH,
        blank=False,
        null=False,
        verbose_name="Название",
        help_text="Название рецепта.",
    )
    image = models.ImageField(
        upload_to="recipes/covers/",
        null=True,
        default=None,
        verbose_name="Иллюстрация",
        help_text="Картинка, иллюстрирующая рецепт.",
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name="Описание",
        help_text="Подробное описание рецепта.",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name="Время приготовления",
        help_text="Время приготовления в минутах.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        null=True,
        blank=False,
        verbose_name="Теги",
        help_text=(
            "Теги, к которым относится рецепт.",
            " Может быть несколько.",
        ),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        help_text=(
            "Ингредиенты — продукты для приготовления блюда по рецепту.",
            " Множественное поле с выбором из предустановленного списка",
            " и с указанием количества и единицы измерения.",
        ),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации рецепта",
        help_text="Присваивается автоматически.",
    )

    class Meta:

        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(models.Model):
    """
    Промежуточная модель для связи рецептов и ингредиентов.
        - Поле recipe связано с моделью Recipe.
        - Поле ingredient связано с моделью Ingredient.
        - Поле value позволяет указать количество ингредиента,
        необходимое для связанного рецепта.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Рецепт",
        help_text="Id рецепта, к которому относится ингредиент.",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Ингредиент",
        help_text="Id ингредиента.",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name="Количество",
        help_text="Количество ингредиента, необходимое для рецепта.",
    )


class ShortenedLinks(models.Model):
    """Модель для хранения пар "длинная ссылка-короткий индекс"."""

    original_url = models.URLField()
    short_link_code = models.CharField(
        max_length=MAX_SHORT_LINK_CODE, unique=True
    )

    def save(self, *args, **kwargs):
        """
        Автоматическое добавление короткого кода.
        Если код уже есть в базе, то код не генерируется.
        """
        if not self.short_link_code:
            self.short_link_code = self.generate_short_code()
        super(ShortenedLinks, self).save(*args, **kwargs)

    def generate_short_code(self):
        """Генератор коротких кодов."""
        characters = string.ascii_letters + string.digits
        while True:
            short_link_code = "".join(
                random.choices(characters, k=MAX_SHORT_LINK_CODE)
            )
            if not ShortenedLinks.objects.filter(
                short_link_code=short_link_code
            ).exists():
                return short_link_code

    def __str__(self):
        return self.original_url
