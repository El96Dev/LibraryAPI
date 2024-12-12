import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

# Authors tests

@pytest.mark.asyncio
async def test_get_empty_authors(client: TestClient):
    response = client.get("/authors")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_nonexistent_author(client: TestClient):
    response = client.get("/authors/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Author with id 1 wasn't found!"}

@pytest.mark.asyncio
async def test_create_author(client: TestClient):
    request_body = {
        "firstname": "John",
        "lastname": "Johnson",
        "birth_date": "1850-10-10"
    }
    response = client.post("/authors", json=request_body)
    assert response.status_code == 201
    assert response.json() == { 
        "id": 1,
        "firstname": "John",
        "lastname": "Johnson",
        "birth_date": "1850-10-10"
    }

@pytest.mark.asyncio
async def test_get_authors_list(client: TestClient):
    request_body = {
        "firstname": "Joe",
        "lastname": "Johnson",
        "birth_date": "1860-10-10"
    }
    client.post("/authors", json=request_body)
    response = client.get("/authors")
    assert response.status_code == 200
    assert response.json() == [
        { 
            "id": 1,
            "firstname": "John",
            "lastname": "Johnson",
            "birth_date": "1850-10-10"
        },
        { 
            "id": 2,
            "firstname": "Joe",
            "lastname": "Johnson",
            "birth_date": "1860-10-10"
        }
    ]

@pytest.mark.asyncio
async def test_put_author(client: TestClient):
    request_body = {
        "firstname": "Piter",
        "lastname": "Piterson",
        "birth_date": "1920-12-21"
    }
    expected_body = {
        "id": 2,
        "firstname": "Piter",
        "lastname": "Piterson",
        "birth_date": "1920-12-21"
    }
    response_put = client.put("/authors/2", json=request_body)
    assert response_put.status_code == 200
    assert response_put.json() == expected_body
    response_get = client.get("/authors/2")
    assert response_get.status_code == 200
    assert response_get.json() == expected_body

@pytest.mark.asyncio
async def test_delete_nonexistent_author(client: TestClient):
    response = client.delete("/authors/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Author with id 3 wasn't found!"}

@pytest.mark.asyncio
async def test_delete_author(client: TestClient):
    response_delete = client.delete("/authors/1")
    assert response_delete.status_code == 204
    response_get = client.get("/authors")
    assert response_get.status_code == 200
    assert response_get.json() == [
        {
            "id": 2,
            "firstname": "Piter",
            "lastname": "Piterson",
            "birth_date": "1920-12-21"
        }
    ]

# Books tests

@pytest.mark.asyncio
async def test_get_empty_books(client: TestClient):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_book_with_nonexisting_author(client: TestClient):
    request_body = {
        "title": "Book 1",
        "description": "Test book 1",
        "quantity": 10,
        "author_id": 3
    }
    response = client.post("/books", json=request_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Author with id 3 wasn't found!"}

@pytest.mark.asyncio
async def test_create_book_with_negative_quantity(client: TestClient):
    request_body = {
        "title": "Book 1",
        "description": "Test book 1",
        "quantity": -5,
        "author_id": 2
    }
    response = client.post("/books", json=request_body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity must be a positive integer!"}

@pytest.mark.asyncio
async def test_create_book(client: TestClient):
    request_body = {
        "title": "Book 1",
        "description": "Test book 1",
        "quantity": 2,
        "author_id": 2
    }
    expected_body = {
        "id": 2,
        "title": "Book 1",
        "description": "Test book 1",
        "quantity": 2,
        "author_id": 2
    }
    response = client.post("/books", json=request_body)
    assert response.status_code == 201
    assert response.json() == expected_body
    response_get = client.get("/books/2")
    assert response_get.status_code == 200
    assert response_get.json() == expected_body

@pytest.mark.asyncio
async def test_get_books_list(client: TestClient):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "title": "Book 1",
            "description": "Test book 1",
            "quantity": 2,
            "author_id": 2
        }
    ]

@pytest.mark.asyncio
async def test_update_book(client: TestClient):
    request_body = {
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 5,
        "author_id": 2
    }
    expected_body = {
        "id": 2,
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 5,
        "author_id": 2
    }
    response = client.put("/books/2", json=request_body)
    assert response.status_code == 200
    assert response.json() == expected_body
    response_get = client.get("/books/2")
    assert response_get.status_code == 200
    assert response_get.json() == expected_body

@pytest.mark.asyncio
async def test_delete_book(client: TestClient):
    response_delete = client.delete("/books/2")
    assert response_delete.status_code == 204
    response_get = client.get("/books/2")
    assert response_get.status_code == 404
    assert response_get.json() == {"detail": "Book with id 2 wasn't found!"}