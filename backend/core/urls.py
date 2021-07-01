from django.urls import path

from views.examiner import (
    ExamGenericAPIView
)


urlpatterns = [
    path('exams', ExamGenericAPIView.as_view()),
]