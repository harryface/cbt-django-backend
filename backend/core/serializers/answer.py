from rest_framework import serializers

from core.models.answer import Answer
from core.models.question import Question


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'taker', 'question', 'answer']
        read_only_fields = ['id', 'taker',]
