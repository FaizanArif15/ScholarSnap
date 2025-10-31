import schedule
import time
from datetime import datetime
from agent import run_agent  # assume this runs summary + email

def job():
    print(f"⏰ Running ScholarSnap agent at {datetime.now()}")
    run_agent()

# Schedule every 5 minutes
schedule.every(5).minutes.do(job)

print("🚀 ScholarSnap Scheduler started (runs every 5 minutes)")
while True:
    schedule.run_pending()
    time.sleep(30)
