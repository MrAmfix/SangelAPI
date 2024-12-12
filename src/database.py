from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.settings import DATABASE_URL


engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    class_=AsyncSession,
)
Base = declarative_base()


# В роутерах будем использовать session: AsyncSession = Depends(get_session)
async def get_session() -> Generator:
    session: AsyncSession = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
