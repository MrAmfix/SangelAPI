from fastapi import Depends
import pytest
import asyncio
from src.models.models import Base
from src.database import SessionLocal
from src.crud import VerificationCodeCrud, VisibilityTypeCrud
from src.utils.enums import DefaultVisibilityType


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

async def change_create_time(session, payload, time_expire_value):
    get_id_query = await VerificationCodeCrud.get_last_code(session=session, phone=payload)
    record = get_id_query
    await VerificationCodeCrud.update(
        session=session, 
        record_id=record.id, 
        created_at=time_expire_value)

async def create_visibility_type(session,):
        await VisibilityTypeCrud.create(
            name=DefaultVisibilityType.ALL,
            session=session
        )

        
def run_async(async_func, *args,**kwargs):
    session = SessionLocal()
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(async_func(session,*args,**kwargs))
    finally:
        loop.run_until_complete(session.close())
