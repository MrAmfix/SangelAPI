from src.crud.base.factory import BaseCrudFactory
from src.models import Notification
from src.schemas import NotificationModels


class NotificationCrud(
    BaseCrudFactory(
        model=Notification,
        update_schema=NotificationModels.Update,
        create_schema=NotificationModels.Create,
        get_schema=NotificationModels.Get
    )
):
    pass
