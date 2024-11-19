from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters, permissions, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView




from .serializers import AvatarSerializer, FollowSerializer
from .permissions import IsSameUserOrRestricted
from .models import Follow

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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.avatar = serializer.validated_data["avatar"]
        user.save()
        return Response(
            {
                "avatar": "Аватар успешно изменен!"
            },  # Изменить ответ, должен выдавать ссылку
            status=status.HTTP_200_OK,
        )


# Отличие от моего вьюсета в том что в ТЗ все должно делаться по ссылке
# вида http://localhost/api/users/{id}/subscribe/ 
# Также другой ответ API
class FollowViewSet(viewsets.GenericViewSet,
                    ListModelMixin,
                    CreateModelMixin,):
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
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=following__username",)
    permission_classes = (
        IsAuthenticated,
        IsSameUserOrRestricted,
    )

    def perform_create(self, serializer):
        """Создает подписку."""
        following_username = self.request.data.get("following")
        following_user = get_object_or_404(User, username=following_username)
        serializer.save(user=self.request.user, following=following_user)

    def get_queryset(self):
        """Возвращает подписки пользователя."""
        user = self.request.user
        return Follow.objects.filter(user=user)
 


class SubscribeViewSet(viewsets.GenericViewSet,
                    CreateModelMixin,):
    """
    """
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=following__username",)
    permission_classes = (
        IsAuthenticated,
        IsSameUserOrRestricted,
    )

    def get_user_id(self):
        """Возвращает id пользователя из URL."""
        return self.kwargs.get("user_id")

    def create(self, request, *args, **kwargs):
        following_id = self.get_user_id()
        print(f"ID: {following_id}")
        # serializer = self.get_serializer(data=request.data)
        following_user = get_object_or_404(User, id=following_id)
        following_username = following_user.username # Тут я подписываюсь по юзернейму - надо это изменить
        data = {
            "user": self.request.user,
            "following": following_username,
        }
        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        print("DATA IS VALID")
        serializer.save(user=self.request.user, following=following_user) # Очень криво но работает

        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Возвращает подписки пользователя."""
        user = self.request.user
        return Follow.objects.filter(user=user)
