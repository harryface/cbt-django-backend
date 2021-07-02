from rest_framework import response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

from cbt.authentication import JWTAuthentication
from core.models import Exam
from core.serializers import (
    ExamSerializerwithQuestions, RegisterStudentsSerializer
    )


class ExamGenericAPIView(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializerwithQuestions


class RegisterStudentsAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        exam = Exam.objects.filter(pk=pk).first()
        if exam:
            serializer = RegisterStudentsSerializer(exam, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(serializer.data)
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(
            {"error": "Exam does not exist"}, status=status.HTTP_404_NOT_FOUND)
