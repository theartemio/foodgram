from django.urls import path

from .views import ManageCartViewSet, ManageFavesViewSet

add_to_favorites = ManageFavesViewSet.as_view({"post": "create"})

add_to_cart = ManageCartViewSet.as_view({"post": "create"})

urlpatterns = [
    path("recipes/<int:recipe_id>/favorite/", add_to_favorites),
    path("recipes/<int:recipe_id>/shopping_cart/", add_to_cart),
]
