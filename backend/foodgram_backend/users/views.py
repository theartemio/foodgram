from django.contrib.auth import get_user_model
from rest_framework import status


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import AvatarSerializer

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
