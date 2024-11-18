from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe

from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from rest_framework import response, viewsets


from .mixins import (GetMixin,
                     PaginationMixin,
                     SearchMixin)  # Для пагинации использовать класс, по умолчанию паагинации не будет


class TagViewSet(GetMixin, viewsets.ModelViewSet):
    """Возвращает список тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(SearchMixin, GetMixin, viewsets.ModelViewSet):
    """Возвращает список ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# Тут нужно сделать чтобы данные возвращались в нужном формате: юзер возвращался в виде
# объекта юзера.
class RecipeViewSet(PaginationMixin, viewsets.ModelViewSet):
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
        """Создает рецепт, указывая отправившего запрос юзера как автора."""
        serializer.save(author=self.request.user)

'''
    def get_queryset(self):
        title_id = self.get_post_id()
        return self.queryset.filter(title_id=title_id)
'''