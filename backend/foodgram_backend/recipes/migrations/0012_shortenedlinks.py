# Generated by Django 3.2.16 on 2024-11-27 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20241126_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField()),
                ('short_link_code', models.CharField(max_length=6, unique=True)),
            ],
        ),
    ]
