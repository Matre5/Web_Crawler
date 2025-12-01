import asyncio
from datetime import datetime
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
        try:
            # fetching
            html = await self.fetcher.fetch(url)
            if html is None:
                logger.error(f"Failed to fetch {url}")
                return

            # HTML snapshot
            await self.db.snapshots.update_one(
                {"url": url},
                {"$set": {"raw_html": html, "timestamp": datetime.utcnow()}},
                upsert=True
            )

           # parsing
            data = self.parser.parse_book_details(html)
            if not data:
                logger.error(f"Failed to parse {url}")
                return

            data["url"] = url
            data["crawl_timestamp"] = datetime.utcnow()

            # checking records
            existing = await self.db.books.find_one({"url": url})
            changes = {}

            if existing:
                track_fields = [
                    "price_including_tax",
                    "price_excluding_tax",
                    "availability",
                    "rating",
                    "num_reviews",
                ]

                for field in track_fields:
                    if data.get(field) != existing.get(field):
                        changes[field] = {
                            "old": existing.get(field),
                            "new": data.get(field),
                        }

                if changes:
                    # Update document
                    await self.db.books.update_one(
                        {"url": url},
                        {"$set": data}
                    )

                    # Log the changes
                    await self.db.changes.insert_one({
                        "book_url": url,
                        "fields_changed": changes,
                        "timestamp": datetime.utcnow()
                    })

                    logger.info(f"Updated → {data['title']} | Changes: {changes}")

                else:
                    logger.info(f"No changes → {data['title']}")

            else:
                # totally new record
                await self.db.books.insert_one(data)

                await self.db.changes.insert_one({
                    "book_url": url,
                    "fields_changed": "new_book_added",
                    "timestamp": datetime.utcnow()
                })

                logger.success(f"New book added → {data['title']}")

        except Exception as e:
            logger.error(f"Error processing {url}: {e}")

    async def run(self):
        logger.info("Worker started. Waiting for tasks...")

        while not self.queue.is_empty():
            url = await self.queue.get_url()
            await self.process_url(url)
            self.queue.task_done()
