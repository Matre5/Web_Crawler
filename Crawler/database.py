from pymongo import MongoClient, errors
from loguru import logger
from datetime import datetime
import os

class Database:
    def __init__(self, uri: str=None, db_name: str = "book_crawler"):
        
        self.uri = uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.client = MongoClient(self.uri)
        self.db = self.client[db_name]
        self.collection = self.db["books"]
        
        self.collection.create_index("source_url", unique=True)
        
    
    def save_book(self, book_data: dict):
        """
        Insert or update a book document.
        Adds metadata if not already present in the database.
        """
        book_data = book_data.copy() 
        book_data.setdefault("crawl_timestamp", datetime.utcnow())
        book_data.setdefault("status", "success")

        source_url = book_data.get("source_url")
        if not source_url:
            logger.error("Book data missing source_url, cannot save.")
            return False

        try:
            result = self.collection.update_one(
                {"source_url": source_url},
                {"$set": book_data},
                upsert=True
            )
            return True
        except errors.DuplicateKeyError:
            logger.warning(f"Duplicate key for {source_url}, skipping")
            return False
        except Exception as e:
            logger.error(f"Failed to save book: {e}")
            return False