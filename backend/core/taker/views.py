from rest_framework import permissions, response, status, views, viewsets

from cbt.authentication import JWTAuthentication
from core.models import Exam, Result
from .serializers import (
        ExamSerializerwithQuestions,
        ResultSerializer, ExamSerializer
    )


class ExamsListAPIView(views.APIView):
    '''List all available exams the student was registered in'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exams = Exam.objects.filter(students=request.user)
        if exams:
            serializer = ExamSerializer(exams)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exams not Found"}, status=status.HTTP_404_NOT_FOUND)


class ExamGetAPIView(views.APIView):
    '''Get a particular exam with all its question'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        exam = Exam.objects.filter(pk=pk).first()
        if exam:
            serializer = ExamSerializerwithQuestions(exam)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)


class ResultsListAPIView(views.APIView):
    '''List all students results'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        result = Result.objects.filter(taker=request.user)
        if result:
            serializer = ResultSerializer(result, many=True)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Results not found"}, status=status.HTTP_404_NOT_FOUND)