from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base.factory import BaseCrudFactory
from src.models import VisibilityType
from src.schemas import VisibilityTypeModels
from src.utils.enums import DefaultVisibilityType


class VisibilityTypeCrud(
    BaseCrudFactory(
        model=VisibilityType,
        update_schema=VisibilityTypeModels.Update,
        create_schema=VisibilityTypeModels.Create,
        get_schema=VisibilityTypeModels.Get
    )
):
    @staticmethod
    async def get_by_enum(enum: DefaultVisibilityType, session: AsyncSession) -> Optional[VisibilityTypeModels.Get]:
        result = await session.execute(
            select(VisibilityType)
            .filter_by(name=enum)
        )
        result = result.scalars().first()

        return VisibilityTypeModels.Get.model_validate(result) if result else None
