from sqlmodel import SQLModel, Field, Relationship, PrimaryKeyConstraint
import uuid
from typing import Optional, List
from enums import PatronStatusEnum, CopyStatusEnum

class Admin(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=1)
    username: str = Field(max_length=50, nullable=False)
    password_hash: str = Field(nullable=False)
    library_name: str = Field(nullable=False)

class Patron(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    phone: str = Field(max_length=10, unique=True, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True)
    status: PatronStatusEnum = Field(max_length=20, nullable=False, default=PatronStatusEnum.IN)
    barcode_path: str = Field(nullable=False)

class Genre(SQLModel, table=True):
    genre_code: str = Field(primary_key=True, nullable=False)
    genre: str = Field(nullable=False, unique=True)

    books: List["Book"] = Relationship(back_populates="genre")

class Book(SQLModel, table=True):
    isbn: str = Field(max_length=13, min_length=10, nullable=False, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    year: int = Field(nullable=False)
    genre_code: Optional[str] = Field(foreign_key="genre.genre_code", nullable=True)
    qty: int = Field(nullable=False)

    genre: Optional[Genre] = Relationship(back_populates="book")
    copies: List["Copy"] = Relationship(back_populates="book")
    writes: List["Writes"] = Relationship(back_populates="book")

class Copy(SQLModel, table=True):
    id: int = Field(nullable=False)
    isbn: str = Field(foreign_key="book.isbn", nullable=False)  
    status: CopyStatusEnum = Field(default=CopyStatusEnum.AV, nullable=False)
    barcode_path: str = Field(nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", "isbn")
    )  

    book: Book = Relationship(back_populates="copies")

class Author(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    first_name: str = Field(nullable=False, max_length=50)
    middle_name: str = Field(nullable=True, max_length=50)
    last_name: str = Field(nullable=False, max_length=50)

    writes: List["Writes"] = Relationship(back_populates="author")

class Writes(SQLModel, table=True):
    author_id: int = Field(foreign_key="author.id", nullable=False)
    book_isbn: str = Field(foreign_key="book.isbn", nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("author_id", "book_isbn"),
    )
    
    author: Author = Relationship(back_populates="writes")
    book: Book = Relationship(back_populates="writes") 