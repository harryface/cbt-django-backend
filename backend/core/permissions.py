from rest_framework import permissions
from core.models.question import Question


class ExamPermission(permissions.BasePermission):
    """
    Allows student to view and retrieve exams they were enrolled for,
    Allows the examiner to see all and perform all actions.
    """

    def has_permission(self, request, view):
        # Only list exams for student
        if request.user.is_authenticated:
            if (request.user.role == "student" and
                    view.action in ["list", "retrieve", "answer", "result"]):
                view.queryset = view.queryset.filter(
                    is_available=True, students=request.user.id).distinct()
                return True
            elif request.user.role == "examiner":
                return True
        return False


class AnswerPermission(permissions.BasePermission):
    """
    If request.data is a list, we will get all the question ids,
    and check if they are part of the exams the student is subscribed to """
    message = "You are not subscribed to some of the "\
                    "exams you are answering the questions for"

    def has_permission(self, request, _):
        if not request.user.is_authenticated:
            return False
        if isinstance(request.data, list):
            questions_id = [data.get("question") for data in request.data]
            return Question.objects.filter(
                pk__in=questions_id, exam__students=request.user).exists()
        else:
            return Question.objects.filter(
                pk=request.data.get("question"), exam__students=request.user).exists()
