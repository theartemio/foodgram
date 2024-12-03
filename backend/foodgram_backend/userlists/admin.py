from django.contrib import admin

from .models import Favorites, ShoppingCart, UserIngredients

admin.site.register(Favorites, admin.ModelAdmin)

admin.site.register(ShoppingCart, admin.ModelAdmin)

admin.site.register(UserIngredients, admin.ModelAdmin)
