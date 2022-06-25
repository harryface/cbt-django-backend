import base64
import jwt

from django.conf import settings
from django.template.loader import get_template
from django.utils.html import strip_tags

from celery import shared_task
from celery.utils.log import get_task_logger

from account.models.reset_password import ResetPasswordRequest
from helpers.email_helper import EmailHelper

logger = get_task_logger(__name__)


@shared_task
def send_password_reset_email(request_id):
    reset_request = ResetPasswordRequest.objects.get(pk=request_id)
    SITE_NAME = getattr(settings, "SITE_NAME", "roxx")
    APP_URL = getattr(settings, "BASE_URL", "https://roxx.com")
    
    secret = settings.SECRET_KEY
    secret_bytes = secret.encode('ascii')
    encryption_secret = base64.b64encode(secret_bytes)
    secret_key = jwt.encode(
        {"request_id": reset_request.pk}, encryption_secret, algorithm="HS256")
    context = {
        "path": f"{APP_URL}/password/forgot?secret={str(secret_key)}",
        "user": reset_request.user
    }

    body_html = get_template(
        "registration/reset_password.html").render(context)
    body_txt = strip_tags(body_html)
    subject = f"Password reset request on {SITE_NAME}!"
    to_emails = [reset_request.user.email]

    EmailHelper.send_mail(subject, body_txt,
            settings.DEFAULT_FROM_EMAIL, to_emails)
