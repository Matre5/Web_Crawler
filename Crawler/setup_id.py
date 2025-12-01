import asyncio
from loguru import logger
from database import MongoDB

async def setup_indexes(self):

    await self.db.books.create_index("url", unique=True)
    await self.db.changes.create_index("timestamp")
    await self.db.snapshots.create_index("url")

    logger.info("Indexed")

    await self.setup_indexes()