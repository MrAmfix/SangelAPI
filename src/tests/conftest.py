import pytest
import asyncio
from src.models.models import Base
from src.database import SessionLocal


async def clear_all_tables():
    async with SessionLocal() as session:
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_all_tables())