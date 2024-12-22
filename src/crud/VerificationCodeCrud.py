from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.base.factory import BaseCrudFactory
from src.models import VerificationCode
from src.schemas import VerificationCodeModels


class VerificationCodeCrud(
    BaseCrudFactory(
        model=VerificationCode,
        update_schema=VerificationCodeModels.Update,
        create_schema=VerificationCodeModels.Create,
        get_schema=VerificationCodeModels.Get
    )
):
    @staticmethod
    async def get_last_code(
            phone: str,
            session: AsyncSession
    ) -> Optional[VerificationCode]:
        result = await session.execute(
            select(VerificationCode)
            .where(VerificationCode.phone == phone)
            .order_by(desc(VerificationCode.created_at))
        )

        return result.scalars().first()
