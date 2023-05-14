import pytest
from starlette.testclient import TestClient

import os
import sys

# previoujs path add
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.main import app

client = TestClient(app)


@pytest.fixture
def test_book_payload():
    """Create test book payload."""
    return {"title": "Test Book", "rating": 5, "author_id": 1}


@pytest.fixture
def test_author_payload():
    """Create test author payload."""
    return {"name": "Test Author", "age": 30}


def test_create_book(test_book_payload):
    response = client.post("/add-book", json=test_book_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["rating"] == 5
    assert data["author_id"] == 1


def test_create_author(test_author_payload):
    response = client.post("/add-author", json=test_author_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Author"
    assert data["age"] == 30


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_authors():
    response = client.get("/authors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
