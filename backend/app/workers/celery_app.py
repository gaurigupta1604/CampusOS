from celery import Celery
from app.core.config import settings
celery_app=Celery("campusos",broker=settings.redis_url,backend=settings.redis_url,include=["app.workers.tasks"])
celery_app.conf.update(task_serializer="json",result_serializer="json",accept_content=["json"],timezone="UTC",task_track_started=True,broker_connection_retry_on_startup=True,beat_schedule={"refresh-analytics":{"task":"analytics.refresh","schedule":3600.0}})
