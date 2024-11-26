from django.contrib.auth import get_user_model
from recipes.models import Recipe
from rest_framework import serializers, status, viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404

from foodgram_backend.utils import get_image_url

User = get_user_model()


class UserRecipeListsMixin:
    """
    Миксин для сериализаторов для описывающих списки рецептов моделей,
    таких как избранное или список покупок.
    Связан с моделями:
        - User
        - Recipe
    Проверяет, не добавляет ли пользователь рецепт в список повторно.
    """

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    def validate(self, data):
        """
        Проверяет что:
            - Пользователь не пытается добавить рецепт в список
            повторно.
        """
        model = self.Meta.model
        user = data["user"]
        if model.objects.filter(user=user, recipe=data["recipe"]).exists():
            raise serializers.ValidationError("Рецепт уже добавлен")

        return data

    def to_representation(self, instance):
        """
        Возвращает добавленный рецепт по нужной форме.
        """
        recipe = instance.recipe
        image_url = get_image_url(recipe.image)
        data = {
            "id": recipe.id,
            "name": recipe.name,
            "image": image_url,
            "cooking_time": recipe.cooking_time,
        }
        return data


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

