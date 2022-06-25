from django.db import models
from django.conf import settings

from helpers.base_model import BaseDateTimeModel


class Answer(BaseDateTimeModel):

    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='user_answers')
    question = models.ForeignKey(
        "core.Question", on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=255)

    class Meta:
        unique_together = ["taker", "question"]
