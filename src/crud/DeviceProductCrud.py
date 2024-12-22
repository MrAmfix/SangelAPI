from src.crud.base.factory import BaseCrudFactory
from src.models import DeviceProduct
from src.schemas import DeviceProductModels


class DeviceProductCrud(
    BaseCrudFactory(
        model=DeviceProduct,
        update_schema=DeviceProductModels.Update,
        create_schema=DeviceProductModels.Create,
        get_schema=DeviceProductModels.Get
    )
):
    pass
