from django.db import models
from django.conf import settings

from helpers.base_model import BaseDateTimeModel


class Result(BaseDateTimeModel):
    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='user_results')
    exam = models.ForeignKey(
        "core.Exam", on_delete=models.PROTECT, related_name='results')
    total_question = models.IntegerField(default=0)
    attempted = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.exam} Result for {self.taker}"

    @property
    def percentage(self):
        return self.correct_answers / (self.total_question or 1) * 100
