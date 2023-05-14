from pydantic import BaseModel, BaseConfig
from typing import Optional


class OrmConfig(BaseConfig):
    """
    Config class for Pydantic models.
    """

    orm_mode = True


class Book(BaseModel):
    """
    Book model class.
    """

    title: str
    rating: Optional[int]
    author_id: Optional[int]

    class Config(OrmConfig):
        pass


class Author(BaseModel):
    """
    Author model class.
    """

    name: str
    age: Optional[int]

    class Config(OrmConfig):
        pass
