from rest_framework import serializers

from account.models import CustomUser
from core.models import Exam, Question, Result, Answer


class QuestionSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''
    
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        exclude = ['exam',]
        read_only_fields = ['created_at', 'updated_at']

    """
    exam_image_url = serializers.SerializerMethodField()
    
    def get_exam_image_url(self, question):
        request = self.context.get('request')
        if question.exam_image and hasattr(question.exam_image, 'url'):
            photo_url = question.exam_image.url
            return request.build_absolute_uri(photo_url)
        else:
            return None
    """
    

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
        fields = ['id', 'title', 'instructions', 'duration', 'is_available', 'questions']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        exam = Exam.objects.create(**validated_data)
        if questions_data:
            Question.objects.bulk_create(
              [
                 Question(exam=exam, **question)
                 for question in questions_data
              ],
            )
        return exam
    
    def update(self, instance, validated_data):

        questions = validated_data.pop('questions')

        for question in questions:
            question_id = question.get('id', None)
            if question_id:
                que = Question.objects.get(id=question_id, exam=instance)
                que.question = question.get('name', que.question)
                que.exam_image = question.get('exam_image', que.exam_image)
                que.option1 = question.get('option1', que.option1)
                que.option2 = question.get('option2', que.option2)
                que.option3 = question.get('option3', que.option3)
                que.option4 = question.get('option4', que.option4)
                que.option5 = question.get('option5', que.option5)
                que.answer = question.get('answer', que.answer)
                que.save()
            else:
                Question.objects.create(exam=instance, **question)

        return super().update(instance, validated_data)


class ExamSerializer(serializers.ModelSerializer):
    '''can only write the answer'''
    
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions', 'duration', 'is_available', 'questions']
        read_only_fields = ['title', 'instructions', 'duration', 'is_available', 'questions']
        
        
class UserSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''
    exam = serializers.PrimaryKeyRelatedField(many=True, queryset=Exam.objects.filter(is_available=True))

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'exam']
        read_only_fields = ['id', 'first_name', 'last_name', 'email',]
        
    def update(self, instance, validated_data):

        exams = validated_data.pop('exam')
        instance.exam.set(exams)
        instance.save()

        return instance


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
    taker_id = serializers.IntegerField()
    exam_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    taker_choice = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Answer(**validated_data)