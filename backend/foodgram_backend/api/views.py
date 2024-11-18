from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe

from .serializers import TagSerializer, Ingredient, RecipeSerializer

class RecipeViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    """
    ViewSet для работы с рецептами.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )


    def perform_create(self, serializer):
        """Создает рецепт, указывая произведение с id, переданным в URL."""
        title_id = self.get_post_id()
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.get_post_id()
        return self.queryset.filter(title_id=title_id)
