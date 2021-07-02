from rest_framework import response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

from cbt.authentication import JWTAuthentication
from account.models import CustomUser
from core.models import Exam
from core.serializers import (
    ExamSerializerwithQuestions, RegisterStudentsSerializer,
    UserSerializer, UserExamsSerializer
    )


class ExamGenericAPIView(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializerwithQuestions


class ListStudentsAPIView(views.APIView):
    '''List all available students to the examiner'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = CustomUser.objects.filter(is_examiner=False)
        if students:
            serializer = UserSerializer(students)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "No Student Found"}, status=status.HTTP_404_NOT_FOUND)


class RegisterStudentsAPIView(views.APIView):
    '''For registering students for exams'''

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


class GetStudentExamAPIView(views.APIView):
    '''List all exam/question/answer of student'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        student = CustomUser.objects.filter(pk=pk).first()
        if student:
            serializer = UserExamsSerializer(student)
            return response.Response(serializer.data)
        return response.Response(
            {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
