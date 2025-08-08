import os
from celery import Celery

REDIS = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("worker", broker=REDIS, backend=REDIS)
celery_app.conf.task_routes = {"app.tasks.*": {"queue": "cleaner"}}

import app.tasks
