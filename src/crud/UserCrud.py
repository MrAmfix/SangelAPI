from src.crud.base.factory import BaseCrudFactory
from src.models.models import User
from src.schemas.system_schemas import UserUpdate, UserCreate, UserGet


class UserCrud(
    BaseCrudFactory(
        model=User,
        update_schema=UserUpdate,
        create_schema=UserCreate,
        get_schema=UserGet
    )
):
    pass
