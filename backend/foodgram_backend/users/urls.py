from django.urls import include, path

from .views import RegistrationAPIView, EmailPassTokenObtainAPIView, ChangePasswordAPIView, UsersMeAPIView


urlpatterns = [
    path("users/", RegistrationAPIView.as_view()),
    path("auth/token/login/", EmailPassTokenObtainAPIView.as_view()),
    path("users/set_password/", ChangePasswordAPIView.as_view()),
    path("users/me", UsersMeAPIView.as_view())
]
