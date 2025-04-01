from src.crud.base.factory import BaseCrudFactory
from src.models import Passport
from src.schemas import PassportModels
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.encrypt import encrypt_data


class PassportCrud(
    BaseCrudFactory(
        model=Passport,
        update_schema=PassportModels.Update,
        create_schema=PassportModels.Create,
        get_schema=PassportModels.Get
    )
):
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> PassportModels.Get:
        validated_data = PassportModels.Create(**kwargs)
        encrypted_data = {k: encrypt_data(v) for k, v in validated_data.model_dump().items()}
        instance = cls.base_model(**encrypted_data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return cls.get_schema.model_validate(instance)
