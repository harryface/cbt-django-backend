from rest_framework import response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

from cbt.authentication import JWTAuthentication
from account.models import CustomUser
from core.models import Exam, Question
from .serializers import (
    ExamResultSerializer, ExamStudentSerializer,
    ExamWithQuestionsSerializer, StudentExamResultSerializer
)


class ExamGenericAPIView(viewsets.ModelViewSet):
    '''
    Get exam with all the question registered to it,
    update the questions list too, deleting too
    '''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamWithQuestionsSerializer


class ExamStudentsGenericAPIView(viewsets.ModelViewSet):
    '''
    Get exam with all the students registered for it,
    update the students list too, deleting too
    '''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamStudentSerializer


class ExamResultAPIView(views.APIView):
    '''Get an exam with all the results associated'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        exams = Exam.objects.filter(pk=pk, is_available=True)
        if exams:
            serializer = ExamResultSerializer(exams)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)


class StudentExamResultAPIView(views.APIView):
    '''Get a student with exam and result populated'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        student = CustomUser.objects.filter(pk=pk, is_available=True)
        if student:
            serializer = StudentExamResultSerializer(student)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
