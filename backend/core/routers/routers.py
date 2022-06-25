from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views.answer import AnswerCreateView
from core.views.exam import ExamViewSet

app_name = 'core'

router = DefaultRouter()
router.register(r'exam', ExamViewSet, basename='exam')

urlpatterns = [
    path('answer/', AnswerCreateView.as_view()),
]

urlpatterns += router.urls
