from src.crud.base.factory import BaseCrudFactory
from src.models import Media
from src.schemas import MediaModels


class MediaCrud(
    BaseCrudFactory(
        model=Media,
        update_schema=MediaModels.Update,
        create_schema=MediaModels.Create,
        get_schema=MediaModels.Get
    )
):
    pass
