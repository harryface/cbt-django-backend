from celery import shared_task
from celery.utils.log import get_task_logger

from account.models.reset_password import ResetPasswordRequest


logger = get_task_logger(__name__)


@shared_task
def expire_the_password_reset_request(request_id: int):
    reset_request = ResetPasswordRequest.objects.get(pk=request_id)
    reset_request.expired = True
    reset_request.save()
