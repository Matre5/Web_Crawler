import asyncio
from loguru import logger

from fetcher import Fetcher
from parser import Parser
from database import MongoDB
from task_queue import URLQueue


class Worker:
    def __init__(self, db: MongoDB, fetcher: Fetcher, parser: Parser, queue: URLQueue):
        self.db = db
        self.fetcher = fetcher
        self.parser = parser
        self.queue = queue

    async def process_url(self, url: str):
        logger.info(f"Processing URL: {url}")

        # Fetch HTML
        html = await self.fetcher.fetch(url)
        if not html:
            logger.error(f"Failed to fetch {url}")
            return

        # Parse data
        data = self.parser.parse_book_details(html)
        if not data:
            logger.error(f"Failed to parse {url}")
            return

        # Add metadata
        data["source_url"] = url
        data["raw_html"] = html

        # Save to database
        saved_book = await self.db.save_books(data)
        await self.db.save_snapshot(url, html)

        logger.success(f"Saved → {saved_book.get('title')}")

    async def run(self):
        logger.info("Worker started. Waiting for tasks...")

        while not self.queue.is_empty():
            url = await self.queue.get_url()
            await self.process_url(url)
            self.queue.task_done()
