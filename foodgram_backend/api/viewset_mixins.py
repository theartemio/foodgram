from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe


class SearchMixin:
    """Миксин для настройки поиска по названию."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class NoPaginationMixin:
    """Миксин отключения пагинации."""

    pagination_class = None


class ManageUserListsViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
):
    """
    Миксин для вьюсетов для работы со списками, такими как
    избранное или список покупок.
    Позволяет добавлять рецепт в список по переданному в
    URL id.
    """

    permission_classes = (IsAuthenticated,)

    def get_recipe_id(self):
        """Возвращает id рецепта из URL."""
        return self.kwargs.get("recipe_id")

    def create(self, request, *args, **kwargs):
        """Добавляет рецепт в список по переданному id"""
        recipe_id = self.get_recipe_id()
        get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user.id
        data = {
            "user": user,
            "recipe": recipe_id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """Удаляет рецепт из списка по переданному id"""
        recipe_id = self.get_recipe_id()
        get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user.id
        queryset = self.get_queryset()
        if queryset.filter(user=user, recipe_id=recipe_id).exists():
            queryset.filter(user=user, recipe_id=recipe_id).delete()
            return Response(
                {"detail": "Рецепт удален из списка."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "Такого рецепта в списке нет!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
