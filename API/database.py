from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "bookstore"

client = None

def get_db():
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGO_URI)
    return client[DB_NAME]
