from django.urls import path

from .views import (
    RegisterAPIView, LoginAPIView, UserDetailAPIView, LogoutAPIView,
    UserInfoUpdateAPIView, UserPasswordUpdateAPIView
)


urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserDetailAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('users/info', UserInfoUpdateAPIView.as_view()),
    path('users/password', UserPasswordUpdateAPIView.as_view()),
]