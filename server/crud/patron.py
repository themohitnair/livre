import logging
from models import Patron
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import NewPatron, PatronByName, PatronByPhone, PatronByEmail, PatronByID
from fastapi import HTTPException, status

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_patron(body: NewPatron, db: AsyncSession):
    patron = Patron(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
    )
    try:
        db.add(patron)
        await db.commit()
        await db.refresh(patron)
        logger.info(f"Patron created: {patron.id} - {patron.first_name} {patron.last_name}")
        return patron
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating patron: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating patron."
        )

async def get_patron_by_id(body: PatronByID, db: AsyncSession):
    try:
        result = await db.execute(select(Patron).where(Patron.id == body.id, Patron.is_active == True))
        patron = result.scalar_one_or_none()
        
        if patron is None:
            logger.warning(f"Patron not found: {body.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active patron not found."
            )
        logger.info(f"Patron retrieved: {patron.id} - {patron.first_name} {patron.last_name}")
        return patron
    except Exception as e:
        logger.error(f"Error retrieving patron by ID: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patron."
        )

async def get_patron_by_name(body: PatronByName, db: AsyncSession):
    try: 
        result = await db.execute(select(Patron).where(
            Patron.first_name == body.first_name,
            Patron.last_name == body.last_name,
            Patron.is_active == True
        ))
        patron = result.scalar_one_or_none()

        if patron is None:
            logger.warning(f"Patron not found by name: {body.first_name} {body.last_name}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active patron not found"
            )
        logger.info(f"Patron retrieved by name: {patron.id} - {patron.first_name} {patron.last_name}")
        return patron
    except Exception as e:
        logger.error(f"Error retrieving patron by name: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patron."
        )

async def get_patron_by_email(body: PatronByEmail, db: AsyncSession):
    try: 
        result = await db.execute(select(Patron).where(Patron.email == body.email, Patron.is_active == True))
        patron = result.scalar_one_or_none()

        if patron is None:
            logger.warning(f"Patron not found by email: {body.email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active patron not found"
            )
        logger.info(f"Patron retrieved by email: {patron.id} - {patron.first_name} {patron.last_name}")
        return patron
    except Exception as e:
        logger.error(f"Error retrieving patron by email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patron."
        )
    
async def get_patron_by_phone(body: PatronByPhone, db: AsyncSession):
    try: 
        result = await db.execute(select(Patron).where(Patron.phone == body.phone, Patron.is_active == True))
        patron = result.scalar_one_or_none()

        if patron is None:
            logger.warning(f"Patron not found by phone: {body.phone}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active patron not found"
            )
        logger.info(f"Patron retrieved by phone: {patron.id} - {patron.first_name} {patron.last_name}")
        return patron
    except Exception as e:
        logger.error(f"Error retrieving patron by phone: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving patron."
        )

async def delete_patron(body: PatronByID, db: AsyncSession):
    try:
        result = await db.execute(select(Patron).where(Patron.id == body.id))
        patron = result.scalar_one_or_none()
        
        if patron is None:
            logger.warning(f"Attempted to delete non-existent patron: {body.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patron not found."
            )

        patron.is_active = False
        await db.commit()
        logger.info(f"Patron marked as inactive: {patron.id} - {patron.first_name} {patron.last_name}")
        return {"detail": "Patron marked as inactive successfully."}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error marking patron as inactive: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error marking patron as inactive."
        )