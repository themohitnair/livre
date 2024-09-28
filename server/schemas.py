from pydantic import BaseModel, Field, constr, EmailStr, field_validator
from typing import Optional
import uuid

# Librarian Schemas
class LibrarianBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=12)

class LibrarianPasswordChange(BaseModel):
    username: constr(min_length=3, max_length=50)
    old_password: constr(min_length=12)
    new_password: constr(min_length=12)

class Token(BaseModel):
    access_token: str
    token_type: str

# Patron Schemas
class PatronBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    email: EmailStr
    phone: constr(min_length=10, max_length=10)

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits.')
        return value

class PatronByName(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]

class PatronByID(BaseModel):
    id: uuid.UUID

class PatronByPhone(BaseModel):
    phone: constr(min_length=10, max_length=10)

    @field_validator('phone')
    def validate_phone(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        return value

class PatronByEmail(BaseModel):
    email: EmailStr
