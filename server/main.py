from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

from routers.author import author_router
from routers.patron import patron_router
from routers.publisher import publisher_router
from routers.borrow import borrow_router
from routers.copy import copy_router
from routers.book import book_router
from crud.librarian import create_librarian, auth_librarian, change_password
from database import init_db, yield_session
from schemas import Token, LibrarianBase, LibrarianPasswordChange, LibrarianAuthBase
from models import Librarian


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(author_router, prefix="/author")
app.include_router(book_router, prefix="/book")
app.include_router(patron_router, prefix="/patron")
app.include_router(publisher_router, prefix="/publisher")
app.include_router(borrow_router, prefix="/borrow")
app.include_router(copy_router, prefix="/copy")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_librarian(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(yield_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    librarian = await auth_librarian(LibrarianAuthBase(username=username), db)
    if librarian is None:
        raise credentials_exception
    return librarian

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(yield_session)):
    librarian = await auth_librarian(LibrarianBase(username=form_data.username, password=form_data.password), db)
    if not librarian:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": librarian.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/configure-librarian")
async def configure_librarian(body: LibrarianBase, db: AsyncSession = Depends(yield_session)):
    return await create_librarian(body, db)

@app.put("/change-password")
async def change_librarian_password(body: LibrarianPasswordChange, librarian: Annotated[Librarian, Depends(get_current_librarian)], db: AsyncSession = Depends(yield_session)):
    return await change_password(body, db)

@app.get("/")
async def greet(librarian: Annotated[Librarian, Depends(get_current_librarian)]):
    return {"message": "hello from livre!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
