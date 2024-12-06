from django.contrib import admin

from .models import Favorites, ShoppingCart

admin.site.register(Favorites, admin.ModelAdmin)

admin.site.register(ShoppingCart, admin.ModelAdmin)
