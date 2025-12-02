from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://aigmatre5_db_user:zByZ6SpZSnZBe41i@cluster001.xiunuvf.mongodb.net/"
DB_NAME = "bookstore"

client = None

def get_db():
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGO_URI)
    return client[DB_NAME]
