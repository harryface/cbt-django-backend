from rest_framework import serializers

from account.models import CustomUser
from core.models import Answer, Exam, Question, Result


class ResultSerializer(serializers.ModelSerializer):
    '''Answer serializer, for viewing'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Result
        exclude = ['taker', 'exam']


class AnswerSerializer(serializers.ModelSerializer):
    '''Answer serializer, for viewing'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Answer
        fields = ['taker_choice', 'is_correct']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        exclude = ['exam', ]
        read_only_fields = ['created_at', 'updated_at']


class QuestionSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        exclude = ['exam', ]
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


class ExamSerializerwithQuestions(serializers.ModelSerializer):
    '''
    Allows both creation and update of the exam
    and questions, for the examiner
    '''

    results = ResultSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'questions', 'results']
        read_only_fields = ['result', 'created_at', 'updated_at']

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


class RegisterStudentsSerializer(serializers.ModelSerializer):
    '''For registering students for an exam'''

    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.filter(is_examiner=False))

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'instructions',
            'duration', 'is_available', 'students']
        read_only_fields = [
            'title', 'instructions', 'duration', 'is_available']

    def update(self, instance, validated_data):

        students = validated_data.pop('students')
        instance.students.set(students)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = ['first_name', 'last_name', 'email', ]


class UserExamsSerializer(serializers.ModelSerializer):

    exams = ExamSerializerwithQuestions(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'exams']
        read_only_fields = ['first_name', 'last_name', 'email', ]


class ExamResultsSerializer(serializers.ModelSerializer):
    '''
    For getting the list of results in an exam
    '''

    questions = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'questions', 'result']
        read_only_fields = '__all__'