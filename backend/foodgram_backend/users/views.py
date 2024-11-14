import random
from django.contrib.auth import get_user_model, password_validation
from rest_framework import status

from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import response, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ValidationError

from .serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    EmailPassTokenObtainSerializer,
    UsersMeSerializer,
)

User = get_user_model()

# Заготовка вью для просмотра профиля пользователя
class UsersViewSet(APIView):
    """
    Вьюсет просмотра списка пользователей администраторами.
    Позволяет админу просматривать список пользователей,
    добавлять новых, удалять старых и менять информацию.
    """

    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    queryset = User.objects.all()
    # serializer_class = UsersSerializer
    # filter_backends = (filters.SearchFilter,)
    lookup_field = "username"
    search_fields = ("username",)


class RegistrationAPIView(APIView):
    """
    Вьюсет для регистрации новых пользователей.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        raw_data = request.data
        serializer = self.serializer_class(data=raw_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(
            serializer.validated_data["password"]
            )
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Работает, но хочу проверить логику и оптимизировать
class EmailPassTokenObtainAPIView(APIView):
    """
    Вьюсет для получения токена с помощью пары Эмейл + Пароль.
    """

    permission_classes = (AllowAny,)
    serializer_class = EmailPassTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        raw_data = request.data
        serializer = self.serializer_class(data=raw_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        password = request.data["password"]
        if not user.check_password(raw_password=password):
            return Response(
                {"error": "Неверно указан пароль!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# Работает, но доделать
class UsersMeAPIView(APIView):
    """
    Позволяет пользователю просматривать информацию о себе и менять ее.
    Просмотр информации и ее изменение доступно только
    самому пользователю.
    Методы:
    Вьюсет работает только с мето
    ами GET и PATCH.
    """

    def get(self, request):
        user = request.user
        serializer = UsersMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Работает, посмотреть еще раз код
class ChangePasswordAPIView(APIView):
    """Вьюсет для смены пароля."""

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    # Работает см коммент
    def post(self, request):
        user = request.user
        
        # Контекст явно передаем в сериализатор, он почему-то не передается так
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(raw_password=current_password):
            return Response(
                {"error": "Неверно указан старый пароль!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {"success": "Пароль успешно изменен!"},
            status=status.HTTP_204_NO_CONTENT,
        )
