import asyncio
from loguru import logger

from fetcher import Fetcher
from parser import Parser
from database import MongoDB
from queue import URLQueue
from worker import Worker

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/category/books_1/"


async def discover_all_book_urls():

    fetcher = Fetcher()
    urls = []

    page = 1
    while True:
        page_url = f"{CATALOGUE_URL}page-{page}.html"
        logger.info(f"Discovering page: {page_url}")

        html = await fetcher.fetch(page_url)

        # Stop when it gets to the end
        if not html:
            logger.info("No more pages found. Discovery complete.")
            break

        parser = Parser()
        book_links = parser.extract_book_links(html)

        if not book_links:
            logger.info("Empty book list. Discovery complete.")
            break

        urls.extend(book_links)
        page += 1

    return urls


async def main():
    logger.info("Starting full crawl...")

    # Discover all book URLs
    all_urls = await discover_all_book_urls()
    logger.success(f"Found {len(all_urls)} books.")

    # Initializing
    queue = URLQueue()
    for url in all_urls:
        queue.add_url(url)

    db = MongoDB()
    fetcher = Fetcher()
    parser = Parser()

    # Create workers
    workers = [
        Worker(db=db, fetcher=fetcher, parser=parser, queue=queue)
        for _ in range(5) 
    ]

    # Start all workers
    tasks = [asyncio.create_task(worker.run()) for worker in workers]
    await asyncio.gather(*tasks)

    logger.success("Crawl completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
