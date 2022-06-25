from rest_framework import viewsets, decorators, response, status
from drf_spectacular.utils import extend_schema

from core.models.answer import Answer
from core.models.exam import Exam
from core.serializers.answer import AnswerSerializer
from core.serializers.exam import ExamSerializer
from core.permissions import ExamPermission


class ExamViewSet(viewsets.ModelViewSet):
    """
    Exam Viewset - Lists all the students exams
    as well as retrieves it.
    For teachers to create/update/delete exam and questions.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [ExamPermission]

    @extend_schema(
        request=AnswerSerializer, responses={200: AnswerSerializer})
    @decorators.action(methods=['GET'], detail=True)
    def result(self, request, pk):
        """
        - for getting the result
        We will run some calcualtions her and use it to populate the serializer
        """
        que = self.get_object().questions.count()
        data = {"total_questions": que, "attempted_questions": 0,
                "correct_answers": 0, "wrong_answers": 0, "percentage": 0}
        answers = Answer.objects.filter(
            taker=request.user, question__exam=pk).select_related("question")
        for answer in answers:
            correct = answer.question.answer.lower() == answer.answer.lower()
            data["attempted_questions"] += 1
            data["correct_answers"] += correct
            data["wrong_answers"] += not correct

        data["percentage"] = (data["correct_answers"]/data["total_questions"]) * 100

        return response.Response(data, status=status.HTTP_200_OK)
