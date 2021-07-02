from rest_framework import routers
from django.urls import path

from account.views import (
    RegisterAPIView, LoginAPIView, UserDetailAPIView, LogoutAPIView,
    UserInfoUpdateAPIView, UserPasswordUpdateAPIView
)

from .views import (
    ExamGenericAPIView, RegisterStudentsAPIView
)

router = routers.DefaultRouter()

router.register(r'exams', ExamGenericAPIView)


urlpatterns = [
    path('user/<int:pk>/exams', RegisterStudentsAPIView.as_view()),
    
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserDetailAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('user/info', UserInfoUpdateAPIView.as_view()),
    path('user/password', UserPasswordUpdateAPIView.as_view()),
    
] + router.urls


