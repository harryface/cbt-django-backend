from rest_framework import routers
from django.urls import path

from account.views import (
    RegisterAPIView, LoginAPIView, UserDetailAPIView,
    LogoutAPIView, UserInfoUpdateAPIView,
    UserPasswordUpdateAPIView, UsersDetailAPIView
)

from .views import (
    ExamGenericAPIView, ExamResultAPIView,
    ExamStudentsGenericAPIView, StudentExamResultAPIView
)


urlpatterns = [
    path('exams/', ExamGenericAPIView.as_view({'get': 'list'})),
    path('exam/<int:pk>', ExamGenericAPIView.as_view(
        {'get': 'retrieve', 'put': 'update', 'post': 'create'})),

    path('student/exams/',
         ExamStudentsGenericAPIView.as_view({'get': 'list'})),
    path('students/exam/<int:pk>/',
         ExamStudentsGenericAPIView.as_view(
             {'get': 'retrieve', 'put': 'update',})),

    path('exam/<int:pk>/results', ExamResultAPIView.as_view()),
    path('student/<int:pk>/perfomance', StudentExamResultAPIView.as_view()),

    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserDetailAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('user/info', UserInfoUpdateAPIView.as_view()),
    path('user/password', UserPasswordUpdateAPIView.as_view()),
    path('users', UsersDetailAPIView.as_view()),

]
