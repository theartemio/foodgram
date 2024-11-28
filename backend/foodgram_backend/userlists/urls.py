from django.urls import path

from api.views import ManageCartViewSet, ManageFavesViewSet

add_to_favorites = ManageFavesViewSet.as_view({"post": "create", "delete": "destroy"})

add_to_cart = ManageCartViewSet.as_view({"post": "create", "delete": "destroy"})

urlpatterns = [
    path("recipes/<int:recipe_id>/favorite/", add_to_favorites),
    path("recipes/<int:recipe_id>/shopping_cart/", add_to_cart),
]
