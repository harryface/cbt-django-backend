from rest_framework import serializers

from core.models.question import Question


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'image', 'question', 'option_1', 'option_2',
                    'option_3', 'option_4', 'option_5', 'answer']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'answer': {'write_only': True}}
