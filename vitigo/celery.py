from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vitigo.settings')  

app = Celery('vitigo')

app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()  
app.conf.beat_schedule = {
    'send-follow-up-reminders-daily': {
        'task': 'appointments.tasks.send_follow_up_reminders',
        'schedule': crontab(hour=5, minute=0), 
    },
    'reset-notification-sent-flag-every-24-hours': {
        'task': 'yourapp.tasks.reset_notification_sent_flag',
        'schedule': crontab(hour=0, minute=0), 
    },
}