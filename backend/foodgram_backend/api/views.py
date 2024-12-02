from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, ShortenedLinks, Tag
from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userlists.models import Favorites, ShoppingCart, UserIngredients
from users.permissions import IsAuthorOrReadOnly

from .filtersets import RecipeFilter
from .mixins import NoPaginationMixin, SearchMixin
from .serializers import (
    FavoritesSerializer,
    IngredientSerializer,
    RecipeAddingSerializer,
    RecipeDetailSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)
from .viewset_mixins import ManageUserListsViewSet


# Вьюсеты для простых моделей
class TagViewSet(
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


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
        recipe = serializer.save(author=self.request.user)
        serializer = RecipeDetailSerializer(
            recipe, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Разрешает PATCH запросы только при передаче полных данных."""
        kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RecipeDetailSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

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
