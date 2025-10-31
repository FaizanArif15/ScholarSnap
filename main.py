# main_scheduler.py
import schedule
import time
from datetime import datetime
from agent import run_agent

INTERVAL_MINUTES = 5

def job():
    print(f"[{datetime.now().isoformat()}] ⏰ Scheduler: running agent...")
    ok = run_agent()
    print(f"[{datetime.now().isoformat()}] ✅ Completed: {ok}")

# schedule job every 5 minutes
schedule.every(INTERVAL_MINUTES).minutes.do(job)

print(f"🚀 Scheduler started — will run every {INTERVAL_MINUTES} minutes.")
# run first time immediately when scheduler starts (optional)
job()

while True:
    schedule.run_pending()
    time.sleep(10)
