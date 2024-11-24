from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AvatarAPIView, SubscribeViewSet

follows = SubscribeViewSet.as_view({
    "get": "list",
})
subscribe = SubscribeViewSet.as_view({
    "post": "create"
}
)


router = DefaultRouter()


urlpatterns = [
    path("users/me/avatar/", AvatarAPIView.as_view()),
    path("users/subscriptions/", follows, name="subscription_list"),
    path("users/<int:user_id>/subscribe/", subscribe),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include("djoser.urls")),
]
