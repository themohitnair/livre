from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint
from typing import List, Optional
from enums import *
import uuid
from passlib.context import CryptContext
from decimal import Decimal
from datetime import datetime, timedelta
import pytz

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

TIMEZONE = pytz.timezone('Asia/Kolkata')

class Patron(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=254, nullable=False, unique=True)
    phone: str = Field(max_length=10, nullable=False, unique=True)
    fine: Decimal = Field(default=Decimal('0.00'), nullable=False)
    status: PatronStatusEnum = Field(default=PatronStatusEnum.IN, nullable=False)
    barcode_path: str = Field(nullable=False)

    borrows: List["Borrow"] = Relationship(back_populates="patron")

class Author(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=30, nullable=False)
    middle_name: str = Field(max_length=30, nullable=True)
    last_name: str = Field(max_length=30, nullable=False)

    books: List["Write"] = Relationship(back_populates="author")

    class Config:
        table_args = (UniqueConstraint('first_name', 'middle_name', 'last_name', name='uq_auth_full_name'),)

class Publisher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)

    books: List["Book"] = Relationship(back_populates="publisher")

    class Config:
        table_args = (UniqueConstraint('name', name='uq_pub_name'),)

class Genre(SQLModel, table=True):
    code: int = Field(default=None, primary_key=True)
    genre: str = Field(nullable=False, max_length=15)

    books: List["Book"] = Relationship(back_populates="genre")

class Write(SQLModel, table=True):
    book_isbn: str = Field(foreign_key="book.isbn", primary_key=True)
    author_id: int = Field(foreign_key="author.id", primary_key=True)

    book: "Book" = Relationship(back_populates="authors")
    author: "Author" = Relationship(back_populates="books")    

class Book(SQLModel, table=True):
    isbn: str = Field(min_length=10, max_length=13, primary_key=True)
    title: str = Field(nullable=False)
    
    genre_code: int = Field(foreign_key="genre.code", nullable=False)
    publisher_id: int = Field(foreign_key="publisher.id", nullable=False)
    qty: int = Field(nullable=False, default=1)

    genre: Genre = Relationship(back_populates="books")
    publisher: Publisher = Relationship(back_populates="books")
    authors: List[Write] = Relationship(back_populates="book")
    copies: List["Copy"] = Relationship(back_populates="book")  

class Copy(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    isbn: str = Field(foreign_key="book.isbn", nullable=False)
    status: str = Field(nullable=False, default="available")
    barcode_path: str = Field(nullable=False)

    book: Book = Relationship(back_populates="copies")

    borrows: List["Borrow"] = Relationship(back_populates="copy")

class Borrow(SQLModel, table=True):
    patron_id: uuid.UUID = Field(foreign_key="patron.id", nullable=False, primary_key=True)
    copy_id: uuid.UUID = Field(foreign_key="copy.id", nullable=False, primary_key=True)
    borrow_date: datetime = Field(default_factory=lambda: datetime.now(TIMEZONE), nullable=False, primary_key=True)    
    due_date: datetime = Field(default_factory=lambda: datetime.now(TIMEZONE) + timedelta(days=15), nullable=False)
    return_date: Optional[datetime] = Field(default=None)

    patron: Patron = Relationship(back_populates="borrows")
    copy: Copy = Relationship(back_populates="borrows")

    class Config:
        table_args = (UniqueConstraint('patron_id', 'copy_id', 'borrow_date', name='uq_borrow'),)

class Librarian(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    hashed_password: str

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)