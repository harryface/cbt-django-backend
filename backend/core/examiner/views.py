from rest_framework import exceptions, response, status, views, viewsets
from rest_framework.permissions import IsAuthenticated

from cbt.authentication import JWTAuthentication
from account.models import CustomUser
from core.models import Exam
from core.serializers import ExamSerializerwithQuestions, UserSerializer


class ExamGenericAPIView(viewsets.ModelViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializerwithQuestions
    
    
class AddStudentExamAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        user = CustomUser.objects.filter(pk=pk).first()
        if user:
            if user.is_examiner:
                raise exceptions.APIException('You cannot assign exams to an examiner!')
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(serializer.data)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({"error" : "student does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
