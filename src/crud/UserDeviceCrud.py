from src.crud.base.factory import BaseCrudFactory
from src.models import UserDevice
from src.schemas import UserDeviceModels


class UserDeviceCrud(
    BaseCrudFactory(
        model=UserDevice,
        update_schema=UserDeviceModels.Update,
        create_schema=UserDeviceModels.Create,
        get_schema=UserDeviceModels.Get
    )
):
    pass
