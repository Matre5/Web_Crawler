import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Settings
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = 'bookstore'
BOOKS_COLLECTION = os.getenv("BOOKS_COLLECTION", "books")

# Crawl Settings
BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/"

# Scheduler Settings
CRAWL_INTERVAL_MINUTES = int(os.getenv("CRAWL_INTERVAL_MINUTES", 60))

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_KEY = os.getenv("API_KEY")
