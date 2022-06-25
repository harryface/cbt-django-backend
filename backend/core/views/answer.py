from rest_framework import generics

from core.models.answer import Answer
from core.serializers.answer import AnswerSerializer
from core.permissions import AnswerPermission


class AnswerCreateView(generics.CreateAPIView):
    """
    for answering questions
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [AnswerPermission, ]

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(taker=self.request.user)
