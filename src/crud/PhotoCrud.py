from src.crud.base.factory import BaseCrudFactory
from src.models.models import Photo
from src.schemas.system_schemas import PhotoUpdate, PhotoCreate, PhotoGet


class PhotoCrud(
    BaseCrudFactory(
        model=Photo,
        update_schema=PhotoUpdate,
        create_schema=PhotoCreate,
        get_schema=PhotoGet
    )
):
    pass
