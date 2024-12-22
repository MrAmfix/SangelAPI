from src.crud.base.factory import BaseCrudFactory
from src.models import Event
from src.schemas import EventModels


class EventCrud(
    BaseCrudFactory(
        model=Event,
        update_schema=EventModels.Update,
        create_schema=EventModels.Create,
        get_schema=EventModels.Get
    )
):
    pass
