from src.crud.base.factory import BaseCrudFactory
from src.models import Observer
from src.schemas import ObserverModels


class ObserverCrud(
    BaseCrudFactory(
        model=Observer,
        update_schema=ObserverModels.Update,
        create_schema=ObserverModels.Create,
        get_schema=ObserverModels.Get
    )
):
    pass
