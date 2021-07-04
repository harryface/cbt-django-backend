from rest_framework import serializers

from account.models import CustomUser as Student
from core.models import Exam, Question, Result
from core.utils import NestedUpdateCreate


class QuestionSerializer(serializers.ModelSerializer):
    '''Question serializer, permits all functions'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        exclude = ['exam', ]
        read_only_fields = ['created_at', 'updated_at']


class ExamWithQuestionsSerializer(serializers.ModelSerializer):
    '''
    Allows both creation and update of the exam
    and questions, for the examiner
    '''

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'questions']
        read_only_fields = ['result', 'created_at', 'updated_at']

    def create(self, validated_data):
        d = NestedUpdateCreate(Exam, Question, 'questions')
        d.create(validated_data)
        return d

    def update(self, instance, validated_data):
        d = NestedUpdateCreate(Exam, Question, 'questions')
        d.update(
            instance, validated_data,
            fields=['title', 'instructions',
                  'duration', 'is_available'])
        
        return super().update(instance, validated_data)


class StudentSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email']
        read_only_fields = ['first_name', 'last_name', 'email', ]


class ExamStudentSerializer(serializers.ModelSerializer):
    '''
    Allows both creation and update of the exam
    and questions, for the examiner
    '''

    students = StudentSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'students']
        read_only_fields = ['id', 'title', 'instructions',
                            'duration', 'is_available']

    def create(self, validated_data):
        d = NestedUpdateCreate(Exam, Student, 'students')
        d.create(validated_data)
        return d

    def update(self, instance, validated_data):
        d = NestedUpdateCreate(Exam, Student, 'students')
        d.update(instance, validated_data)
        return super().update(instance, validated_data)


class ExamResultSerializer(serializers.ModelSerializer):
    '''
    Allows both creation and update of the exam
    and questions, for the examiner
    '''

    class Meta:
        model = Exam
        fields = ['id', 'title', 'instructions',
                  'duration', 'is_available', 'results']
        read_only_fields = '__all__'
        depth = 1


class ResultSerializer(serializers.ModelSerializer):
    '''Just for displaying result with the exam ID'''

    class Meta:
        model = Result
        exclude = ['taker', ]
        read_only_fields = '__all__'


class StudentExamResultSerializer(serializers.ModelSerializer):
    '''Displays Student, Result, exam'''

    result = ResultSerializer(many=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'result']
        read_only_fields = '__all__'
