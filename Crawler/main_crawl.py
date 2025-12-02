import sys
import os

# Add the Crawler root folder to Python path
sys.path.append(os.path.dirname(__file__))

import asyncio
from Utilities.logger import logger
from fetcher import Fetcher
from parser import Parser
from database import MongoDB
from task_queue import URLQueue
from worker import Worker
from urllib.parse import urljoin
from Utilities.config import BASE_URL, CATALOGUE_URL
from Utilities.fetch import fetch



async def discover_all_book_urls():

    urls = []

    page = 1
    while True:
        page_url = f"{CATALOGUE_URL}page-{page}.html"
        logger.info(f"Discovering page: {page_url}")

        html = await fetch(page_url)

        # Stop when it gets to the end
        if not html:
            logger.info("No more pages")
            break

        parser = Parser()
        raw_links = parser.extract_book_links(html)

        if not raw_links:
            logger.info("Empty book list. Finished.")
            break


        full_links = [urljoin(page_url, link) for link in raw_links]

        urls.extend(full_links)
        page += 1

    return urls



async def main():
    logger.info("Let's crawllll...")

    # All books url
    all_urls = await discover_all_book_urls()
    logger.success(f"Found {len(all_urls)} books.")

    # Initializing
    queue = URLQueue()
    for url in all_urls:
        await queue.add_url(url)

    db = MongoDB()
    fetcher = Fetcher()
    parser = Parser()

    # Create workers
    workers = [
        Worker(db=db, fetcher=fetcher, parser=parser, queue=queue)
        for _ in range(1) 
    ]

    # Start all workers
    tasks = [asyncio.create_task(worker.run()) for worker in workers]
    await asyncio.gather(*tasks)

    logger.success("Crawl completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
