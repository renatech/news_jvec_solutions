from __future__ import absolute_import, unicode_literals
import os

from celery.schedules import crontab
from celery import Celery

from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Beat settings
app.conf.beat_schedule = {
    'run-every-5-minutes' : {
        'task' : 'NewsApp.tasks.get_data_from_hacker_news',
        'schedule': crontab(minute='*/5'),   # Execute
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
