from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager

username = "root"
password = "mohitnair"
host = "localhost"
port = 3306
schema_name = "livre"

mysql_url = f"mysql+asyncmy://{username}:{password}@{host}:{port}/{schema_name}"

engine = create_async_engine(mysql_url, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def yield_session():
    async with AsynSession(engine) as session:
        yield session