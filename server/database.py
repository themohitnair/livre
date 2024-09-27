from sqlmodel import create_engine
from models import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
host = "localhost"
port = os.getenv("DATABASE_PORT")
schema_name = "livre"

mysql_url = f"mysql+asyncmy://{username}:{password}@{host}:{port}/{schema_name}"

engine = create_async_engine(mysql_url, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def yield_session():
    async with AsyncSession(engine) as session:
        yield session