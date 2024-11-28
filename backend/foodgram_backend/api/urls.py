from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                    download_shopping_list)

router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("recipes/download_shopping_cart/", download_shopping_list),
    path("", include(router.urls)),
    path("", include("users.urls")),
    path("", include("userlists.urls")),
]
