from src.crud.base.factory import BaseCrudFactory
from src.models import Passport
from src.schemas import PassportModels


class PassportCrud(
    BaseCrudFactory(
        model=Passport,
        update_schema=PassportModels.Update,
        create_schema=PassportModels.Create,
        get_schema=PassportModels.Get
    )
):
    pass
