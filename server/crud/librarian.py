from models import Librarian
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import LibrarianBase, LibrarianPasswordChange, LibrarianAuthBase
from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_librarian(body: LibrarianBase, db: AsyncSession):
    result = await db.execute(select(Librarian))
    existing_librarian = result.scalar_one_or_none()

    if existing_librarian:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A librarian account already exists."
        )

    librarian = Librarian(
        username=body.username, 
        hashed_password=Librarian.get_password_hash(body.password)
    )
    
    db.add(librarian)
    await db.commit() 
    await db.refresh(librarian) 
    return librarian

async def auth_librarian(body: LibrarianAuthBase, db: AsyncSession):
    result = await db.execute(select(Librarian).where(Librarian.username == body.username))
    librarian_admin = result.scalar_one_or_none()

    if not librarian_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Librarian account not found."
        )

    return librarian_admin

async def change_password(body: LibrarianPasswordChange, db: AsyncSession):
    result = await db.execute(select(Librarian).where(Librarian.username == body.username))
    librarian_admin = result.scalar_one_or_none()

    if not librarian_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Librarian account not found."
        )

    if librarian_admin.verify_password(body.old_password):
        librarian_admin.hashed_password = Librarian.get_password_hash(body.new_password)
        await db.commit()
        return {"message": "Password updated successfully"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect old password",
        headers={"WWW-Authenticate": "Bearer"},
    )