from django.contrib import admin

from .models import Ingredient, Recipe, ShortenedLinks, Tag

admin.site.register(Tag)

admin.site.register(Ingredient)

admin.site.register(Recipe)

admin.site.register(ShortenedLinks)
