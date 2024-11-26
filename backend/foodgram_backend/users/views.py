from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .permissions import IsSameUserOrRestricted
from .serializers import (
    AvatarSerializer,
    FollowSerializer,
    SubscriptionsUsersSerializer,
)

User = get_user_model()


class AvatarAPIView(APIView):
    """Вьюсет для загрузки и удаления аватара."""

    serializer_class = AvatarSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save()
        return Response(
            {"avatar": "Аватар успешно удален!"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        user.avatar = serializer.validated_data["avatar"]
        user.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SubscribeViewSet(
    viewsets.GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
):
    """
        Позволяет просматривать свои подписки и подписываться на других.

    Пермишены:
        Просмотр подписок и добавление новой подписки доступно только
        самому пользователю.
        Проверка осуществляется с помощью кастомного пермишена
        IsSameUserOrRestricted.
    Методы:
        Вьюсет работает только с методами GET и POST.
    Поиск:
        Поиск настроен для поиска по точному юзернейму.
    """

    filter_backends = (filters.SearchFilter,)
    search_fields = ("=following__username",)
    permission_classes = (
        IsAuthenticated,
        IsSameUserOrRestricted,
    )

    def get_serializer_class(self):
        if self.action == "list":
            return SubscriptionsUsersSerializer
        return FollowSerializer

    def get_queryset(self):
        """Возвращает подписки пользователя."""
        user = self.request.user
        return CustomUser.objects.filter(following__user=user)

    def get_user_id(self):
        """Возвращает id пользователя из URL."""
        return self.kwargs.get("user_id")

    def create(self, request, *args, **kwargs):
        """Создает подписку по переданному id"""
        following_id = self.get_user_id()
        following_user = get_object_or_404(User, id=following_id)
        data = {
            "user": self.request.user,
            "following": following_id,
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, following=following_user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
