# celery_app.py
from pytz import HOUR
from celery import Celery
import os
from celery.schedules import crontab    

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

interval_minutes = int(os.getenv("INTERVAL_MINUTES", 24))

app = Celery("scholarsnap", broker=broker_url, backend=backend_url)
# app.conf.timezone = "UTC"
app.conf.timezone = 'Asia/Karachi'
app.conf.enable_utc = False
# app.autodiscover_tasks(["tasks"])
app.conf.beat_schedule = {
    "run-agent-every-specific-minutes": {
        "task": "tasks.run_agent_task",
        "schedule": crontab(minute=0, hour="*/1"),
    },
}

import tasks