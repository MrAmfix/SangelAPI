from src.crud.base.factory import BaseCrudFactory
from src.models import Card
from src.schemas import CardModels
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.encrypt import encrypt_data


class CardCrud(
    BaseCrudFactory(
        model=Card,
        update_schema=CardModels.Update,
        create_schema=CardModels.Create,
        get_schema=CardModels.Get
    )
):
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> CardModels.Get:
        validated_data = CardModels.Create(**kwargs)
        encrypted_data = {k: encrypt_data(v) for k, v in validated_data.model_dump().items()}
        instance = cls.base_model(**encrypted_data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return cls.get_schema.model_validate(instance)
