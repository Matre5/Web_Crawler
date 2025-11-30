import asyncio

class URLQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_url(self, url: str):
        # Add a new URL to the queue.
        await self.queue.put(url)

    async def get_url(self) -> str:
        # Retrieve the next URL from the queue.
        return await self.queue.get()

    def task_done(self):
        # Mark a URL as processed.
        self.queue.task_done()

    def is_empty(self) -> bool:
        # Check if the queue is empty.
        return self.queue.empty()

    def size(self) -> int:
        # Return current queue size.
        return self.queue.qsize()