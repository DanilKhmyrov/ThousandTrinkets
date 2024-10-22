import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

app = Celery('online_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_shopping_cart': {
        'task': 'users.tasks.clear_old_shopping_cart',
        'schedule': crontab(hour=0, minute=0),
    },
}
