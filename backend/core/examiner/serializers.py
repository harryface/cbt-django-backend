from rest_framework import serializers

from account.models import CustomUser
from core.models import Exam, Question, Result


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
        # depth = 1

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


class StudentSerializer(serializers.ModelSerializer):
    '''Read only User serializer'''

    id = serializers.IntegerField(required=False)

    class Meta:
        model = CustomUser
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

    """
    def get_or_create_students(self, students):
        student_ids = []
        for student in students:
            student_instance, created = CustomUser.objects.get_or_create(pk=student.get('id'), defaults=student)
            student_ids.append(student_instance.pk)
        return student_ids

    def create_or_update_packages(self, students):
        student_ids = []
        for student in students:
            package_instance, created = CustomUser.objects.update_or_create(pk=student.get('id'), defaults=student)
            student_ids.append(package_instance.pk)
        return student_ids

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        exam = Exam.objects.create(**validated_data)
        exam.students.set(self.get_or_create_packages(students))
        return exam
    """

    def update(self, instance, validated_data):
        students = validated_data.pop('students', [])
        instance.students.set(self.create_or_update_packages(students))
        """
        # Core model fields
        fields = ['order_id', 'is_cod']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
        """
        instance.save()
        return instance


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


class StudentExamResultSerializer(serializers.ModelSerializer):
    '''Displays Student, Result, exam'''

    result = ResultSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'result']
        read_only_fields = ['first_name', 'last_name', 'email', ]