from rest_framework import serializers
from django.db import transaction

from core.models.exam import Exam
from core.models.question import Question
from core.serializers.question import QuestionSerializer


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'duration', 'instructions',
                  'questions', 'students', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'students': {'write_only': True}}

    def create(self, validated_data):
        """
        ModelSerializer .create() method override in order to
        enable nested object bulk creation. All the operations
        are atomic to prevent undesired objects of being saved
        into the DB.
        """
        questions = validated_data.pop('questions', None)
        with transaction.atomic():
            exam = super(ExamSerializer, self).create(
                validated_data)

            for question in questions:
                question['exam'] = exam
                QuestionSerializer().create(question)

        return exam

    def update(self, instance, validated_data):
        """
        ModelSerializer .update() method override in order to
        enable nested bulk updating of legs. All the operations
        are atomic to prevent undesired objects of being saved
        into the DB.
        """
        questions = validated_data.pop('questions', [])
        errors = []
        with transaction.atomic():
            for question in questions:
                if 'id' in question:
                    try:
                        ExamSerializer().update(
                            instance.scheduled_legs.get(pk=question['id']), question)
                    except Question.DoesNotExist:
                        errors.append(
                            {question['id']: (
                                "The question provided does not belong to this exam or doesn't exist.")
                             }
                        )
                else:
                    QuestionSerializer().create(question)

            if errors:
                raise serializers.ValidationError(
                    "One or more exam were invalid. " + str(errors))

            trip = super(ExamSerializer, self).update(instance, validated_data)

        return trip

