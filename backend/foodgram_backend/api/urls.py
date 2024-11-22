from django.urls import include, path

from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, IngredientViewSet, RecipeViewSet)

router = DefaultRouter()
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include("users.urls")),
    path("", include("shoppinglist.urls")),
]
