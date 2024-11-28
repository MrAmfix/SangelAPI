from src.crud.base.factory import BaseCrudFactory
from src.models.models import Notification
from src.schemas.system_schemas import NotificationUpdate, NotificationCreate, NotificationGet


class NotificationCrud(
    BaseCrudFactory(
        model=Notification,
        update_schema=NotificationUpdate,
        create_schema=NotificationCreate,
        get_schema=NotificationGet
    )
):
    pass
