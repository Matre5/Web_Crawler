import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("API_KEY")
HEADERS = {"entry_key": API_KEY}

@pytest.mark.parametrize("limit,page", [(1, 1), (5, 1)])
def test_get_books(limit, page):
    resp = requests.get(f"{BASE_URL}/books?limit={limit}&page={page}", headers=HEADERS)
    assert resp.status_code == 200
    books = resp.json()
    assert isinstance(books, list)
    if books:
        assert "id" in books[0]
        assert "title" in books[0]

def test_get_book_by_valid_id_dynamic():
    # Get a book ID dynamically
    resp = requests.get(f"{BASE_URL}/books?limit=1&page=1", headers=HEADERS)
    assert resp.status_code == 200
    books = resp.json()
    assert len(books) > 0
    book_id = books[0]["id"]

    # Test /books/{book_id}
    resp2 = requests.get(f"{BASE_URL}/books/{book_id}", headers=HEADERS)
    assert resp2.status_code == 200
    book = resp2.json()
    assert book["id"] == book_id
    assert "title" in book
    assert "price" in book

def test_get_book_invalid_id():
    resp = requests.get(f"{BASE_URL}/books/invalid_id_123", headers=HEADERS)
    assert resp.status_code == 200
    assert "error" in resp.json()

def test_search_books():
    resp = requests.get(f"{BASE_URL}/books/search?q=history", headers=HEADERS)
    assert resp.status_code == 200
    results = resp.json()
    assert isinstance(results, list)
    for book in results:
        assert "id" in book
        assert "title" in book

def test_list_categories():
    resp = requests.get(f"{BASE_URL}/categories", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "categories" in data
    assert isinstance(data["categories"], list)

def test_stats_endpoint():
    resp = requests.get(f"{BASE_URL}/stats", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "books" in data
    assert "changes_logged" in data

def test_changes_endpoint():
    resp = requests.get(f"{BASE_URL}/changes?limit=5", headers=HEADERS)
    assert resp.status_code == 200
    logs = resp.json()
    assert isinstance(logs, list)

def test_health_endpoint():
    resp = requests.get(f"{BASE_URL}/health", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
