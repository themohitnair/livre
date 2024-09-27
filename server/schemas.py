from pydantic import BaseModel, Field, constr

class LibrarianBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=12)

class LibrarianAuthBase(BaseModel):
    username: constr(min_length=3, max_length=50)

class LibrarianPasswordChange(BaseModel):
    username: constr(min_length=3, max_length=50)
    old_password: constr(min_length=12)
    new_password: constr(min_length=12)

class Token(BaseModel):
    access_token: str
    token_type: str