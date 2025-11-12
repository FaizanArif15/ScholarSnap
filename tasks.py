# tasks.py
from celery_app import app
from agent import run_agent
from db import init_db
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# @app.task
# def run_agent_task():
#     print("🚀 Initializing database...")
#     init_db()
#     print("🚀 Running scheduled task: run_agent")
#     result = run_agent()
#     print("✅ Task finished:", result)
#     return result


@app.task(
    
)
def run_agent_task():
    logs = []
    logs.append("🚀 Initializing database...")
    init_db()
    logs.append("✅ Database initialized")
    logs.append("🚀 Running agent")
    result = run_agent()
    logs.append(f"✅ Task finished: {result}")
    return "\n".join(logs)