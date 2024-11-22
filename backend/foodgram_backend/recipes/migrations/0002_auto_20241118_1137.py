# Generated by Django 3.2.16 on 2024-11-18 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time',
            new_name='cooking_time',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text=('Уникальный слаг, по которому можно указать тег', 'Рекомендуется использовать понятный слаг,', ' например транслитерацию или английское название.'), max_length=150, unique=True, verbose_name='Слаг'),
        ),
    ]