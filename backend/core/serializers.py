from rest_framework import serializers

from account.models import CustomUser
from core.models import Exam, Question, Result, Answer


class UserSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''

    exam_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_exam_image_url(self, question):
        request = self.context.get('request')
        if question.exam_image and hasattr(question.exam_image, 'url'):
            photo_url = question.exam_image.url
            return request.build_absolute_uri(photo_url)
        else:
            return None


class TakerQuestionSerializer(serializers.ModelSerializer):
    '''The taker can read all but can only write the answer'''

    exam_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2', 'option3',
                  'option4', 'option5', 'get_exam_image_url', 'answer']
        read_only_fields = ['question', 'option1', 'option2', 'option3',
                            'option4', 'option5', 'get_exam_image_url']
        extra_kwargs = {
            'answer': {'write_only': True}
        }

    def get_exam_image_url(self, question):
        request = self.context.get('request')
        if question.exam_image and hasattr(question.exam_image, 'url'):
            photo_url = question.exam_image.url
            return request.build_absolute_uri(photo_url)
        else:
            return None


class ExamSerializerwithQuestions(serializers.ModelSerializer):
    '''
    Allows both creation and update of the exam
    and questions, for the examiner
    '''

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    # def create(self, validated_data):
    #     questions_data = validated_data.pop('questions', [])
    #     exam = Exam.objects.create(**validated_data)
    #     if questions_data:
    #         Question.objects.bulk_create(
    #           [
    #              Question(exam=exam, **question)
    #              for question in questions_data
    #           ],
    #         )
    #     return exam


class ExamSerializer(serializers.ModelSerializer):
    '''can only write the answer'''

    questions = TakerQuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    '''For viewing results'''

    taker = UserSerializer()
    exam = ExamSerializer()

    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    taker = UserSerializer()
    exam = ExamSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = {'taker_choice'}


class TakerAnswerSerialiszer(serializers.Serializer):
    taker_id = serializers.PrimaryKeyRelatedField()
    exam_id = serializers.PrimaryKeyRelatedField()
    question_id = serializers.PrimaryKeyRelatedField()
    taker_choice = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Answer(**validated_data)