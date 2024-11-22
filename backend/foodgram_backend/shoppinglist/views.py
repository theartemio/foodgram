from django.contrib.auth import get_user_model


from .serializers import FavoritesSerializer, ShoppingCartSerializer


from .mixins import ManageUserListsViewSet

User = get_user_model()


class ManageFavesViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком избранного"""

    serializer_class = FavoritesSerializer


class ManageCartViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком покупок"""

    serializer_class = ShoppingCartSerializer
