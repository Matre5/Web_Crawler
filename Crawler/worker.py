import time
from loguru import logger

from fetcher import Fetcher
from parser import Parser
from database import MongoDB  


class Worker:
    def __init__(self, db: MongoDB, fetcher: Fetcher, parser: Parser):
        self.db = db
        self.fetcher = fetcher
        self.parser = parser

    def process_task(self, task):
        task_id, url, status = task
        logger.info(f"Processing task {task_id}: {url}")

        # Mark as processing
        self.db.update_task_status(task_id, "processing")

        # Fetch HTML
        html = self.fetcher.fetch(url)
        if not html:
            logger.error(f"Failed to fetch {url}")
            self.db.update_task_status(task_id, "failed")
            return

        # Parse HTML
        data = self.parser.parse_book_details(html)
        if not data:
            logger.error(f"No data parsed for {url}")
            self.db.update_task_status(task_id, "failed")
            return

        # metadata
        data["source_url"] = url
        data["raw_html"] = html

        # Saving to db
        self.db.save_book(data)
        self.db.save_snapshot(url, html)

        
        self.db.update_task_status(task_id, "done")
        logger.success(f"Task {task_id} completed → {data.get('title')}")

    def run(self):
        logger.info("Worker started. Waiting for tasks...")

        while True:
            task = self.db.get_next_task()

            if not task:
                logger.info("No tasks found. Sleeping for 3 seconds...")
                time.sleep(3)
                continue

            self.process_task(task)
