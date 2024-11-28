from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, ShortenedLinks, Tag
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (action, api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userlists.models import Favorites, ShoppingCart, UserIngredients
from users.permissions import IsAuthorOrReadOnly

from .filtersets import RecipeFilter
from .mixins import NoPaginationMixin, SearchMixin
from .serializers import (FavoritesSerializer, IngredientSerializer,
                          RecipeAddingSerializer, RecipeDetailSerializer,
                          RecipeIngredientSerializer, ShoppingCartSerializer,
                          TagSerializer)
from .viewset_mixins import ManageUserListsViewSet


# Вьюсеты для простых моделей
class TagViewSet(
    UpdateModelMixin,  # Отключить
    CreateModelMixin,  # Отключить
    NoPaginationMixin,
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    """Возвращает список тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(
    # CreateModelMixin,
    SearchMixin,
    NoPaginationMixin,
    RetrieveModelMixin,
    ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


# Вьюсеты для пользовательских списков
class ManageFavesViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком избранного"""

    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()


class ManageCartViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком покупок"""

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()


class RecipeViewSet(
    viewsets.ModelViewSet,
):
    """
    ViewSet для работы с рецептами.
    """

    queryset = Recipe.objects.all()
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = RecipeAddingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    ordering_fields = ("-pub_date",)

    def list(self, request, *args, **kwargs):
        """Выдача объектов списком по нужной форме."""
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RecipeDetailSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
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

        if not ingredient_list:
            return Response(
                {"ingredients": "Список ингредиентов не может быть пустым!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Вынести в функцию
        for ingredient in ingredient_list:
            ingredient_serializer = RecipeIngredientSerializer(data=ingredient)
            ingredient_serializer.is_valid(raise_exception=True)
            try:
                current_ingredient = get_object_or_404(
                    Ingredient, id=ingredient["id"]
                )
            except Http404:
                return Response(
                    {"error": "Ингредиент не найден!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ingredient_serializer.save(
                ingredient=current_ingredient, recipe=recipe
            )
        serializer = RecipeDetailSerializer(
            recipe, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        if "ingredients" not in serializer.validated_data.keys():
            return Response(
                {"error": "Поле ингредиенты обязательно!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "tags" not in serializer.validated_data.keys():
            return Response(
                {"error": "Поле ингредиенты обязательно!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ingredient_list = serializer.validated_data.pop("ingredients")
        recipe = serializer.save(author=self.request.user)
        for ingredient in ingredient_list:
            ingredient_serializer = RecipeIngredientSerializer(data=ingredient)
            ingredient_serializer.is_valid(raise_exception=True)
            try:
                current_ingredient = get_object_or_404(
                    Ingredient, id=ingredient["id"]
                )
            except Http404:
                return Response(
                    {"error": "Ингредиент не найден!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ingredient_serializer.save(
                ingredient=current_ingredient, recipe=recipe
            )

        self.perform_update(serializer)
        serializer = RecipeDetailSerializer(
            recipe, context={"request": request}
        )

        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="get-link")
    def get_link(self, request, pk):
        """Создает постоянную короткую ссылку для рецепта."""
        long_url = request.get_full_path().replace("get-link/", "")
        url, created = ShortenedLinks.objects.get_or_create(
            original_url=long_url
        )
        short_code = url.short_link_code
        short_path = reverse("short-link", kwargs={"short_code": short_code})
        short_link = request.build_absolute_uri(short_path)
        response = Response(
            {"short-link": short_link},
            status=status.HTTP_200_OK,
        )
        return response


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download_shopping_list(request):
    """Возвращает список покупок в виде списка в формате rtf."""
    user = request.user
    users_ingredients = UserIngredients.objects.filter(user=user.id)
    formatted_lines = [
        f"{i.ingredient.name}, ({i.ingredient.measurement_unit}) - {i.total}"
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
