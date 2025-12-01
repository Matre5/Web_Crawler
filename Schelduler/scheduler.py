import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..Crawler import main_crawl
import subprocess
from datetime import datetime
import json
from loguru import logger
from ..Crawler import database

# DAILY CHANGE REPORT FILE
REPORT_PATH = "daily_change_report.json"


async def generate_daily_report():

    db = database.MongoDB()
    since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    cursor = db.changes.find({"timestamp": {"$gte": since}})
    changes = await cursor.to_list(length=None)

    report = {
        "date": since.isoformat(),
        "total_changes": len(changes),
        "changes": changes,
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, default=str, indent=4)

    logger.success(f"Daily report → {REPORT_PATH}")

async def scheduled_crawl():
    print("Starting scheduled crawl...")
    await main_crawl.main()
    print("Scheduled crawl completed!")

def start_scheduler():
    scheduler = AsyncIOScheduler()

    # Scheduled for 5am
    scheduler.add_job(lambda: asyncio.create_task(scheduled_crawl()), 'cron', hour= 5)

    scheduler.start()
    print("Scheduler activated and running...")

    try:
        asyncio.get_event_loop().run_forever() 
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()
