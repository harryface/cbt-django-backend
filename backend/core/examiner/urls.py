from rest_framework import routers
from django.urls import path

from account.views import (
    RegisterAPIView, LoginAPIView, UserDetailAPIView, LogoutAPIView,
    UserInfoUpdateAPIView, UserPasswordUpdateAPIView
)

from .views import (
    ExamGenericAPIView, RegisterStudentsAPIView,
    ListStudentsAPIView, GetStudentExamAPIView,
    ExamResultsAPIView
)

router = routers.DefaultRouter()

router.register(r'exams', ExamGenericAPIView)


urlpatterns = [
    path('exam/<int:pk>/students', RegisterStudentsAPIView.as_view()),
    path('student/<int:pk>/perfomance', GetStudentExamAPIView.as_view()),
    path('all/students', ListStudentsAPIView.as_view()),
    path('exam/<int:pk>/results', ExamResultsAPIView.as_view()),
    
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserDetailAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('user/info', UserInfoUpdateAPIView.as_view()),
    path('user/password', UserPasswordUpdateAPIView.as_view()),
    
] + router.urls


