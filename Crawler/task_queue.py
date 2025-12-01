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
        self.queue.task_done()

    def is_empty(self) -> bool:
        return self.queue.empty()

    def size(self) -> int:
        return self.queue.qsize()