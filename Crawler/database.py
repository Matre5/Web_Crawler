from pymongo import ReturnDocument
from Utilities.logger import logger
from Utilities.config import MONGO_URI
from datetime import datetime
import motor.motor_asyncio

class MongoDB:
    def __init__(self, uri: str = MONGO_URI, db_name: str = "bookstore"):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.books = self.db["books"]
        self.snapshots = self.db["snapshots"]
        self.tasks = self.db['tasks']
        self.changes = self.db["changes"]
    async def save_books(self, book_data:dict):
        
        book_data["last_crawled"] = datetime.utcnow()
        
        filter_key = {
            'title' : book_data['title'],
            'category' : book_data['category']
        }
        
        updated_book = await self.books.find_one_and_update(
            filter_key,
            {'$set': book_data},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        
        return updated_book
    
    async def save_snapshot(self, url:str, html:str):
        
        snapshot = {
            'url': url,
            'html' : html,
            'timestamp' : datetime.utcnow()
        }
        await self.snapshots.insert_one(snapshot)

    async def get_next_task(self):
        return await self.tasks.find_one_and_update(
            {"status": "pending"},
            {"$set": {"status": "processing"}},
            sort=[("created_at", 1)],
            return_document=ReturnDocument.AFTER
        )

