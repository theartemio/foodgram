from django.shortcuts import get_object_or_404
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from rest_framework.response import Response
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeDetailSerializer,
    RecipeIngredientSerializer,
)
from shoppinglist.models import ShoppingCart
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, viewsets
from rest_framework import status
from django.http import HttpResponse
from shoppinglist.models import UserIngredients

from .mixins import (
    GetMixin,
    PaginationMixin,
    SearchMixin,
)  # Для пагинации использовать класс, по умолчанию паагинации не будет


class TagViewSet(GetMixin, viewsets.ModelViewSet):
    """Возвращает список тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(SearchMixin, GetMixin, viewsets.ModelViewSet):
    """Возвращает список ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


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
        serializer = RecipeDetailSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeDetailSerializer(
            recipe, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):
        raw_data = request.data
        serializer = self.serializer_class(data=raw_data)
        serializer.is_valid(raise_exception=True)
        ingredient_list = serializer.validated_data.pop("ingredients")
        recipe = serializer.save(author=self.request.user)
        for ingredient in ingredient_list:
            ingredient_serializer = RecipeIngredientSerializer(data=ingredient)
            ingredient_serializer.is_valid(raise_exception=True)
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient["id"]
            )
            ingredient_serializer.save(
                ingredient=current_ingredient, recipe=recipe
            )
        serializer = RecipeDetailSerializer(
            recipe, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_shopping_list(request):
    """Возвращает список покупок в виде списка в формате rtf."""
    user = request.user
    users_ingredients = UserIngredients.objects.filter(user=user.id)
    formatted_lines = [
        f"{i.ingredient.name}, ({i.ingredient.measure_unit}) - {i.total}"
        for i in users_ingredients
    ]
    response_data = "\n".join(formatted_lines)

    response = HttpResponse(
        response_data,
        headers={
            "Content-Type": "text/rtf",
            "Content-Disposition": 'attachment; filename="list.rtf"',
        },
    )
    return response
