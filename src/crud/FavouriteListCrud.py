from src.crud.base.factory import BaseCrudFactory
from src.models.FavouriteList import FavouriteList
from src.schemas.system_schemas import FavouriteListUpdate, FavouriteListCreate, FavouriteListGet


class FavouriteListCrud(
    BaseCrudFactory(
        model=FavouriteList,
        update_schema=FavouriteListUpdate,
        create_schema=FavouriteListCreate,
        get_schema=FavouriteListGet
    )
):
    pass
