from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from rest_framework.response import Response
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer
from rest_framework import response, viewsets
from rest_framework import status

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

    def list(self, request, *args, **kwargs):
        """Выдача объектов списом по нужной форме."""
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
            # serializer = TitleDetailSerializer(page, many=True)
            # return self.get_paginated_response(serializer.data)
        serializer = RecipeDetailSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data) 
    

    def create(self, request):
        raw_data = request.data
        serializer = self.serializer_class(data=raw_data)
        serializer.is_valid(raise_exception=True)
        ingredient_list = serializer.validated_data.pop("ingredients")
        recipe = serializer.save(author=self.request.user)
        for ingredient in ingredient_list: # Тут проверку надо сделать по сериализатору
            
            current_ingredient = get_object_or_404(Ingredient, id=ingredient["id"])


            value = ingredient["value"]
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe, value=value)




        return Response(
                {"ok": "ok"},
                status=status.HTTP_200_OK,
            )

    def perform_create(self, serializer):
        """Создает рецепт, указывая отправившего запрос юзера как автора."""
        serializer.save(author=self.request.user)

'''
    def get_queryset(self):
        title_id = self.get_post_id()
        return self.queryset.filter(title_id=title_id)
'''