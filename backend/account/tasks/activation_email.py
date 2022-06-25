from django.conf import settings
from django.template.loader import get_template
from django.utils.html import strip_tags

from celery import shared_task
from celery.utils.log import get_task_logger


from account.models.customer import Customer
from helpers.email_helper import EmailHelper


logger = get_task_logger(__name__)


@shared_task
def send_activation_email(pk):
    profile = Customer.objects.get(pk=pk)
    site = getattr(settings, "BASE_URL", "https://roxx.com")
    SITE_NAME = getattr(settings, "SITE_NAME", "roxx")
    path = f"{site}/activate/?key={profile.activation_key}/"
    context = {
        "path": path,
        "user": profile.owner
    }
    body_html = get_template(
        "registration/verify_email.html").render(context)
    body_txt = strip_tags(body_html)
    subject = f"Email Verification on {SITE_NAME}"
    to_emails = [profile.owner.email]
    EmailHelper.send_mail(subject, body_txt,
            settings.DEFAULT_FROM_EMAIL, to_emails, body_html)
