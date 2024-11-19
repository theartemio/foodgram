from django.urls import include, path

from .views import AvatarAPIView
from .views import FollowViewSet


follows = FollowViewSet.as_view({
    "get": "list",
    "post": "create"
})


urlpatterns = [
    path("users/me/avatar/", AvatarAPIView.as_view()),
    path("auth/", include("djoser.urls.authtoken")),
    path("follow/", follows, name="follow"), 
    path("", include("djoser.urls")),
]
