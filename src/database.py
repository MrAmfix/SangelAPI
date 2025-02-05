from typing import Generator

from sqlalchemy.event import listens_for
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.settings import DATABASE_URL


engine = create_async_engine(DATABASE_URL, future=True)


@listens_for(engine.sync_engine, "connect")
def test_connection(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("SELECT 1")
    cursor.close()


SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False,
                                  autoflush=False, class_=AsyncSession, future=True)


async def get_session() -> Generator:
    session: AsyncSession = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
