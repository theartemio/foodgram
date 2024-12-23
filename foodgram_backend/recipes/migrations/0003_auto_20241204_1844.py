# Generated by Django 3.2.16 on 2024-12-04 15:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Время приготовления в минутах.', validators=[django.core.validators.MinValueValidator(1, 'Время приготовления не может быть меньше 1!')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, help_text='Картинка, иллюстрирующая рецепт.', upload_to='recipes/covers/', verbose_name='Иллюстрация'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(help_text='Id рецепта, к которому относится ингредиент.', null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
