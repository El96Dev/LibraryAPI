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
        "id": 1,
        "title": "Book 1",
        "description": "Test book 1",
        "quantity": 2,
        "author_id": 2
    }
    response = client.post("/books", json=request_body)
    assert response.status_code == 201
    assert response.json() == expected_body
    response_get = client.get("/books/1")
    assert response_get.status_code == 200
    assert response_get.json() == expected_body

@pytest.mark.asyncio
async def test_get_books_list(client: TestClient):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
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
        "id": 1,
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 5,
        "author_id": 2
    }
    response = client.put("/books/1", json=request_body)
    assert response.status_code == 200
    assert response.json() == expected_body
    response_get = client.get("/books/1")
    assert response_get.status_code == 200
    assert response_get.json() == expected_body

@pytest.mark.asyncio
async def test_delete_book(client: TestClient):
    response_delete = client.delete("/books/1")
    assert response_delete.status_code == 204
    response_get = client.get("/books/1")
    assert response_get.status_code == 404
    assert response_get.json() == {"detail": "Book with id 1 wasn't found!"}

# Borrows tests

@pytest.mark.asyncio
async def test_get_empty_borrows(client: TestClient):
    response = client.get("/borrows")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_nonexistent_borrow(client: TestClient):
    response = client.get("/borrows/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Borrow with id 1 wasn't found!"}

@pytest.mark.asyncio
async def test_create_borrow_with_nonexistent_book(client: TestClient):
    request_body = {
        "book_id": 5,
        "reader": "Sam Piters",
        "issue_date": "2024-12-12"
    }
    response = client.post("/borrows", json=request_body)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book with id 5 wasn't found!"}

@pytest.mark.asyncio
async def test_create_borrow(client: TestClient):
    book_request_body = {
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 1,
        "author_id": 2
    }
    client.post("/books", json=book_request_body)
    borrow_request_body = {
        "book_id": 2,
        "reader": "Sam Piters",
        "issue_date": "2024-12-12"
    }
    response = client.post("/borrows", json=borrow_request_body)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "book_id": 2,
        "reader": "Sam Piters",
        "issue_date": "2024-12-12",
        "return_date": None
    }
    response_get_book = client.get("/books/2")
    assert response_get_book.status_code == 200
    assert response_get_book.json() == {
        "id": 2,
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 0,
        "author_id": 2
    }

@pytest.mark.asyncio
async def test_get_borrows_list(client: TestClient):
    response = client.get("/borrows")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "book_id": 2,
            "reader": "Sam Piters",
            "issue_date": "2024-12-12",
            "return_date": None
        }
    ]

@pytest.mark.asyncio
async def test_update_borrow_with_incorrect_datetime(client: TestClient):
    request_body = {
        "return_date": "2024-08-23"
    }
    response = client.patch("/borrows/1", json=request_body)
    assert response.status_code == 409
    assert response.json() == {"detail": "The return date must be later than the issue date!"}

@pytest.mark.asyncio
async def test_update_borrow(client: TestClient):
    request_body = {
        "return_date": "2024-12-20"
    }
    response = client.patch("/borrows/1", json=request_body)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "book_id": 2,
        "reader": "Sam Piters",
        "issue_date": "2024-12-12",
        "return_date": "2024-12-20"
    }
    response_get_book = client.get("/books/2")
    assert response_get_book.status_code == 200
    assert response_get_book.json() == {
        "id": 2,
        "title": "Book 2",
        "description": "Test book 2",
        "quantity": 1,
        "author_id": 2
    }


@pytest.mark.asyncio
async def test_update_closed_borrow(client: TestClient):
    request_body = {
        "return_date": "2024-12-20"
    }
    response = client.patch("/borrows/1", json=request_body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Return date is already set!"}

@pytest.mark.asyncio
async def test_create_borrow_with_issued_book(client: TestClient):
    borrow_request_body = {
        "book_id": 2,
        "reader": "John Johns",
        "issue_date": "2024-12-12"
    }
    first_response = client.post("/borrows", json=borrow_request_body)
    assert first_response.status_code == 201
    second_response = client.post("/borrows", json=borrow_request_body)
    assert second_response.status_code == 409
    assert second_response.json() == {"detail": "Library is out of book with id 2!"}