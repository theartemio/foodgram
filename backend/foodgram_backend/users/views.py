from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from .models import CustomUser, Follow
from .permissions import IsSameUserOrRestricted
from .serializers import (
    AvatarSerializer,
    FollowSerializer,
    SubscriptionsUsersSerializer,
)
from djoser.views import UserViewSet

User = get_user_model()

class CustomUserViewSet(UserViewSet):
    def me(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Вход не выполнен!"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return super().me(request, *args, **kwargs)

class AvatarAPIView(APIView):
    """
    Вьюсет для загрузки и удаления аватара.
    Позволяет аутентифицированному (пермишен IsAuthenticated)
    пользователю изменять собственный аватар.
    Методы:
        - Вьюсет работает только с методами POST и DELETE.
    """

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
    Вьюсет для работы с моделью подписок.
    Позволяет просматривать свои подписки и подписываться на других.

    Пермишены:
        - Просмотр подписок и добавление новой подписки доступно только
        самому пользователю.
        - Проверка осуществляется с помощью кастомного пермишена
        IsSameUserOrRestricted.
    Методы:
        - Вьюсет работает только с методами GET, POST, DELETE.
    Поиск:
        - Поиск настроен для поиска по точному юзернейму.
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
        user_serializer = SubscriptionsUsersSerializer(
            following_user, context={"request": request}
        )
        return Response(
            user_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        """Удаляет подписку из списка по переданному id"""
        following_id = self.get_user_id()
        user_id = self.request.user.id
        try:
            instance = get_object_or_404(
                Follow, user=user_id, following_id=following_id
            )
        except Http404:
            return Response(
                {"error": "Такой подписки не существует!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return Response(
            {"detail": "Подписка удалена."},
            status=status.HTTP_204_NO_CONTENT,
        )
