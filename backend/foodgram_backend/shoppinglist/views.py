from django.contrib.auth import get_user_model

from .viewset_mixins import ManageUserListsViewSet
from .serializers import FavoritesSerializer, ShoppingCartSerializer
from .models import Favorites, ShoppingCart

User = get_user_model()


class ManageFavesViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком избранного"""

    serializer_class = FavoritesSerializer
    queryset = Favorites.objects.all()


class ManageCartViewSet(ManageUserListsViewSet):
    """Вьюсет для работы со списком покупок"""

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
