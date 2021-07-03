from rest_framework import serializers

from core.models import Answer, Exam, Question, Result


class AnswerSerializer(serializers.ModelSerializer):
    '''Answer serializer, for viewing'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Result
        exclude = ['taker', 'exam']
        extra_kwargs = {
            'taker': {'write_only': True},
            'exam': {'write_only': True}
        }


class ResultSerializer(serializers.ModelSerializer):
    '''Answer serializer, for viewing'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Result
        exclude = ['taker', 'exam']


class QuestionSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        exclude = ['exam', ]
        read_only_fields = ['created_at', 'updated_at']


class ExamSerializerwithQuestions(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'questions', 'result']
        read_only_fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'questions', 'result']
        read_only_fields = '__all__'
