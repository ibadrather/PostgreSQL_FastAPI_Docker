from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import Optional
from app.base import Base


class Book(Base):
    """
    Book model class.
    """

    __tablename__ = "book"
    id: Optional[int] = Column(Integer, primary_key=True, index=True)
    title: Optional[str] = Column(String)
    rating: Optional[int] = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    author_id: Optional[int] = Column(Integer, ForeignKey("author.id"))

    def __init__(self, title: str, rating: int, author_id: int):
        self.title = title
        self.rating = rating
        self.author_id = author_id

    def set_author(self, author: "Author"):
        """
        Set the author of the book.
        """
        self.author = relationship("Author", back_populates="books")


class Author(Base):
    """
    Author model class.
    """

    __tablename__ = "author"
    id: Optional[int] = Column(Integer, primary_key=True)
    name: Optional[str] = Column(String)
    age: Optional[int] = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    books = relationship("Book", back_populates="author")

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
