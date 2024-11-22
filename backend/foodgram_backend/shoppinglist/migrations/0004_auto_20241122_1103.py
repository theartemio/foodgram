# Generated by Django 3.2.16 on 2024-11-22 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_rename_quantity_recipeingredient_value'),
        ('shoppinglist', '0003_auto_20241121_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(help_text='Id рецепта, к которому относится ингредиент.', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]