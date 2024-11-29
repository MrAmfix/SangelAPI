from src.crud.base.factory import BaseCrudFactory
from src.models import FavouriteContact
from src.schemas import FavouriteContactModels


class FavouriteContactCrud(
    BaseCrudFactory(
        model=FavouriteContact,
        update_schema=FavouriteContactModels.Update,
        create_schema=FavouriteContactModels.Create,
        get_schema=FavouriteContactModels.Get
    )
):
    pass
