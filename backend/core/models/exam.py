from django.db import models
from django.conf import settings

from helpers.base_model import BaseDateTimeModel


class Exam(BaseDateTimeModel):
    '''Database model for examination'''
    title = models.CharField(unique=True, max_length=255)
    is_available = models.BooleanField(default=True)
    duration = models.PositiveIntegerField('Time in seconds', default=60)
    instructions = models.TextField(default='')
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="core.Result")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
