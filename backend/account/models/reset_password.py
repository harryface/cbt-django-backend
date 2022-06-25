from django.db import models
from django.conf import settings

from helpers.base_model import BaseDateTimeModel


class ResetPasswordRequest(BaseDateTimeModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE, null=True, blank=True)
    used = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
