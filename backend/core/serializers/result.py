from rest_framework import serializers

from core.models.result import Result


class ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Result
        fields = ['id', 'taker', 'exam', 'total_question', 'attempted',
                    'correct_answers', 'wrong_answers', 'percentage']
        read_only_fields = ['id', 'percentage']
