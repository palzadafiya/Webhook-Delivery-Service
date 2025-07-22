from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "webhook_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30,  # 30 seconds
    task_soft_time_limit=25,  # 25 seconds
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,
    beat_schedule={
        'cleanup-old-logs': {
            'task': 'app.tasks.delivery_tasks.cleanup_old_logs',
            #'schedule': crontab(hour=0, minute=0),  # Run daily at midnight UTC
            # Alternatively, you can use:
             'schedule': 60,  # Run every 86400 seconds (24 hours)
        },
    }
)

# Import tasks to ensure they're registered
from app.tasks import delivery_tasks