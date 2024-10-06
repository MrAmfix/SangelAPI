from src.crud.base.factory import BaseCrudFactory
from src.models.UserStatus import UserStatus
from src.schemas.system_schemas import UserStatusUpdate, UserStatusCreate, UserStatusGet


class UserStatusCrud(
    BaseCrudFactory(
        model=UserStatus,
        update_schema=UserStatusUpdate,
        create_schema=UserStatusCreate,
        get_schema=UserStatusGet
    )
):
    pass
