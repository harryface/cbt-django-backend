from django.urls import path

from account.views import (
    RegisterAPIView, LoginAPIView, UserDetailAPIView, LogoutAPIView,
    UserInfoUpdateAPIView, UserPasswordUpdateAPIView
)

from .views import (
    ExamsListAPIView, ExamGetAPIView, ResultsListAPIView
)


urlpatterns = [
    path('exams', ExamsListAPIView.as_view()),
    path('exam/<int:pk>', ExamGetAPIView.as_view()),
    path('results', ResultsListAPIView.as_view()),

    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserDetailAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('user/info', UserInfoUpdateAPIView.as_view()),
    path('user/password', UserPasswordUpdateAPIView.as_view()),
    
    # path('exams', ExamGenericAPIView.as_view()),
]