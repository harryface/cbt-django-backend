from django.urls import path

from core.views.examiner import (
    ExamGenericAPIView
)


urlpatterns = [
    path('exams', ExamGenericAPIView.as_view()),
]