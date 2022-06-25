import logging, os
from celery import Celery

logger = logging.getLogger("Celery")
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roxx.config.base')
 
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
