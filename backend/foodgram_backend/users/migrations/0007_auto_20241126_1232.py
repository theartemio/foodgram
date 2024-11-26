# Generated by Django 3.2.16 on 2024-11-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20241126_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(help_text="Имя. Полное или ваше любимое сокращение, например 'Васёк'.", max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(help_text='Фамилия. Настоящая или выдуманная.', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Уникальный юзернейм (никнейм, псевдоним).', max_length=150, unique=True, verbose_name='Юзернейм'),
        ),
    ]