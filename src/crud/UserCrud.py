from src.crud.base.factory import BaseCrudFactory
from src.models import User
from src.schemas import UserModels


class UserCrud(
    BaseCrudFactory(
        model=User,
        update_schema=UserModels.Update,
        create_schema=UserModels.Create,
        get_schema=UserModels.Get
    )
):
    pass
