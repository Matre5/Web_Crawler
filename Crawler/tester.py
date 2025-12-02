import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from Utilities.config import DB_NAME, MONGO_URI
import os


async def test_atlas_connection():
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]

        # List collections (should be empty if first run)
        collections = await db.list_collection_names()
        print(f"Connected successfully! Collections: {collections}")

        result = await db["test_collection"].insert_one({"test": "ok"})
        print(f"Test document inserted with ID: {result.inserted_id}")

        await db["test_collection"].delete_one({"_id": result.inserted_id})
        print("Test document deleted. Connection works perfectly!")

    except Exception as e:
        print(f"Failed to connect: {e}")

# Run the test
asyncio.run(test_atlas_connection())
