from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework import serializers, status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram_backend.utils import get_image_url

User = get_user_model()

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
        user = self.request.user.id
        queryset = self.get_queryset()
        instance = queryset.get(user=user, recipe_id=recipe_id)
        instance.delete()
        return Response(
            {
                "detail": "Страница не найдена."
            }, status=status.HTTP_404_NOT_FOUND
        )

