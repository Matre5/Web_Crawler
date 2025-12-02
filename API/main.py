import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Query, Security, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from bson import ObjectId
from bson.errors import InvalidId
from Utilities.config import API_KEY
from database import get_db

db =  get_db()
app = FastAPI(title="Web Crawlerrr", version="1.0")


API_KEY_NAME = "entry_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

#validation
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate API key"
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


def normalize_doc(doc):
    
    if isinstance(doc, list):
        return [normalize_doc(item) for item in doc]

    if isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                
                if key == "_id":
                    new_doc["id"] = str(value)
                else:
                    new_doc[key] = str(value)
            else:
                new_doc[key] = normalize_doc(value)
        return new_doc

    return doc

def selected_fields(book):
    return {
        "id": str(book["_id"]),
        "title": book.get("title"),
        "price": book.get("price_including_tax"),
        "availability": book.get("availability"),
        "rating": book.get("rating"),
        "category": book.get("category"),
        "url": book.get("url"),
    }

@app.get("/health")
async def health(api_key: str = Depends(get_api_key)):
    return {"status":"ok"}


@app.get("/books", description="Return books in a certain number of books per pagecd.")
async def get_books(
    limit: int = 20, 
    page: int = 1, 
    api_key: str = Depends(get_api_key)):
    
    skip = (page - 1) * limit
    books = await db.books.find().sort("title", 1).skip(skip).limit(limit).to_list(None)
    
    book_list = [selected_fields(book) for book in books]

    return normalize_doc(book_list)

@app.get("/books/search", description="Return specific book based on requests .")
async def search_books(
    q: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    rating: int | None = None,
    limit: int = 20,
    api_key: str = Depends(get_api_key)
):
    query = {}

    # Search by title
    if q:
        query["title"] = {"$regex": q, "$options": "i"}

    # Filter by category
    if category:
        query["category"] = category

    # Rating filter
    if rating:
        query["rating"] = rating

    # Price range filter
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price_including_tax"] = price_filter

    # Fetch results
    results = await db.books.find(query).limit(limit).to_list(None)

    # Selected output
    S_Output = [
        {
            "id": str(book["_id"]),
            "title": book.get("title"),
            "price": book.get("price_including_tax"),
            "rating": book.get("rating"),
            "category": book.get("category"),
        }
        for book in results
    ]

    return normalize_doc(S_Output)

@app.get("/books/{book_id}", description="Retrieves a book by its id number.")
async def get_book(book_id: str, api_key: str = Depends(get_api_key)):
    try:
        obj_id = ObjectId(book_id)
    except InvalidId:
        return {'error': 'invalid id'}
        
    book = await db.books.find_one({"_id": obj_id}) 
    if not book:
        return {"error": "Book not found"}
    
    book_list = selected_fields(book)

    return normalize_doc(book_list)

@app.get("/categories", description="Return all available categories.")
async def list_categories(api_key: str = Depends(get_api_key)):
    categories = await db.books.distinct("category")
    return {"categories": categories}


@app.get("/changes", description="Return count of changes made.")
async def changes(limit: int = 30, api_key: str = Depends(get_api_key)):
    logs = await db.changes.find().sort("timestamp", -1).limit(limit).to_list(None)
    return normalize_doc(logs)

@app.get("/stats", description="Return total books and changes logged.")
async def stats(api_key: str = Depends(get_api_key)):
    total_books = await db.books.count_documents({})
    total_changes = await db.changes.count_documents({})
    return {
        "books": total_books,
        "changes_logged": total_changes
    }

