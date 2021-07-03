from rest_framework import response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

from cbt.authentication import JWTAuthentication
from core.models import Exam, Result
from .serializers import (
    ExamSerializerwithQuestions,
    ResultSerializer, ExamSerializer
    )


class ExamsListAPIView(views.APIView):
    '''List all available students to the examiner'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exams = Exam.objects.filter(students=request.user)
        if exams:
            serializer = ExamSerializer(exams)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exams not Found"}, status=status.HTTP_404_NOT_FOUND)


class ExamGetAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        exam = Exam.objects.filter(pk=pk).first()
        if exam:
            serializer = ExamSerializerwithQuestions(exam)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)


class ResultsListAPIView(views.APIView):
    '''List all exam/question/answer of student'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        result = Result.objects.filter(taker=request.user).first()
        if result:
            serializer = ResultSerializer(result)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)