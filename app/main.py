import uvicorn
from fastapi import FastAPI

from app.schemas import Book as BookSchema
from app.schemas import Author as AuthorSchema

from app.models import Book, Author

from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# add middleware
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
async def root():
    return {"Status": "It's working!"}


@app.post("/add-book", response_model=BookSchema)
async def add_book(book: BookSchema):
    db_book = Book(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()

    return db_book

@app.post("/add-author", response_model=AuthorSchema)
async def add_author(author: AuthorSchema):
    db_author = Author(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()

    return db_author

@app.get("/books", response_model=list[BookSchema])
async def get_books():
    books = db.session.query(Book).all()
    return books

@app.get("/authors", response_model=list[AuthorSchema])
async def get_authors():
    authors = db.session.query(Author).all()    
    return authors
