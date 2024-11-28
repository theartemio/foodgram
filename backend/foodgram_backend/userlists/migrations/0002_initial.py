# Generated by Django 3.2.16 on 2024-11-28 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0002_initial'),
        ('userlists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='useringredients',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(help_text='Id рецепта, добавленного в список.', on_delete=django.db.models.deletion.CASCADE, related_name='userlists_shoppingcart_list', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(help_text='Id пользователя, добавившего рецепт в список.', on_delete=django.db.models.deletion.CASCADE, related_name='userlists_shoppingcart_owner', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(help_text='Id рецепта, добавленного в список.', on_delete=django.db.models.deletion.CASCADE, related_name='userlists_favorites_list', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AddField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(help_text='Id пользователя, добавившего рецепт в список.', on_delete=django.db.models.deletion.CASCADE, related_name='userlists_favorites_owner', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='useringredients',
            constraint=models.UniqueConstraint(fields=('user', 'ingredient'), name='unique_user_ingredient_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_user_recipe_favorite'),
        ),
    ]