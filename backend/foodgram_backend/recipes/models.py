from django.db import models
from foodgram_backend.constants import MAX_NAMES_LENGTH, MAX_SLUG_LENGTH
from django.contrib.auth import get_user_model
from .mixins import NameMixin

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

    measure_unit = models.CharField(
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
    Модель связана с моделями Tag, User, Ingredient:




        - Поле tag (необязательное) связано с моделью Category,
        - Поле author genre (необязательное) связано с моделью Genre,
        - Поле ingredient
        у одного рецепта допускается несколько тегов,
        переданных списком.
        У одного рецепта допускается несколько ингредиентов,
        переданных ...
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
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Подробное описание рецепта.",
    )
    cooking_time = models.PositiveSmallIntegerField(  # Мб что-то типа datetime minutes
        verbose_name="Время приготовления",
        help_text="Время приготовления в минутах.",
        # validators=(validate_year,),
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
        through="RecipeIngredient",  # Указание промежуточной модели
        help_text=(
            "Ингредиенты — продукты для приготовления блюда по рецепту.",
            " Множественное поле с выбором из предустановленного списка",
            " и с указанием количества и единицы измерения.",
        ),
    )

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(models.Model):
    """
    Промежуточная модель для связи рецептов и ингредиентов.
        - Поле recipe связано с моделью Recipe,
        - Поле ingredient связано с моделью Ingredient,
        - Поле value позволяет указать количество ингредиента
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
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Количество ингредиента, необходимое для рецепта.",
    )
