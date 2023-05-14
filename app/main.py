import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary models and schemas
from app.schemas import Book as BookSchema
from app.schemas import Author as AuthorSchema
from app.models import Book, Author

# Import the DBSessionMiddleware for handling database sessions
from fastapi_sqlalchemy import DBSessionMiddleware, db

from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Add middleware for handling database sessions
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root() -> dict:
    """
    Root GET request.

    Returns:
        dict: A message indicating the API is working.
    """
    return {"Status": "It's working!"}


@app.post("/add-book", response_model=BookSchema)
async def add_book(book: BookSchema) -> BookSchema:
    """
    Endpoint to add a book to the database.

    Args:
        book (BookSchema): The book details.

    Returns:
        BookSchema: The details of the added book.
    """
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    try:
        db.session.add(db_book)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        db.session.close()

    return db_book


@app.post("/add-author", response_model=AuthorSchema)
async def add_author(author: AuthorSchema) -> AuthorSchema:
    """
    Endpoint to add an author to the database.

    Args:
        author (AuthorSchema): The author details.

    Returns:
        AuthorSchema: The details of the added author.
    """
    db_author = Author(name=author.name, age=author.age)
    try:
        db.session.add(db_author)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    finally:
        db.session.close()

    return db_author


@app.get("/books", response_model=List[BookSchema])
async def get_books() -> List[BookSchema]:
    """
    Endpoint to fetch all books from the database.

    Returns:
        List[BookSchema]: A list of books.
    """
    try:
        books = db.session.query(Book).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    return books


@app.get("/authors", response_model=List[AuthorSchema])
async def get_authors() -> List[AuthorSchema]:
    """
    Endpoint to fetch all authors from the database.

    Returns:
        List[AuthorSchema]: A list of authors.
    """
    try:
        authors = db.session.query(Author).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    return authors


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
