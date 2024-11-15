from django.urls import include, path

from .views import AvatarAPIView

urlpatterns = [
    path("users/me/avatar/", AvatarAPIView.as_view()),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
]
