from src.crud.base.factory import BaseCrudFactory
from src.models.DeviceProduct import DeviceProduct
from src.schemas.system_schemas import DeviceProductUpdate, DeviceProductCreate, DeviceProductGet


class DeviceProductCrud(
    BaseCrudFactory(
        model=DeviceProduct,
        update_schema=DeviceProductUpdate,
        create_schema=DeviceProductCreate,
        get_schema=DeviceProductGet
    )
):
    pass
