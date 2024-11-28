from src.crud.base.factory import BaseCrudFactory
from src.models.models import VisibilityType
from src.schemas.system_schemas import VisibilityTypeUpdate, VisibilityTypeCreate, VisibilityTypeGet


class VisibilityTypeCrud(
    BaseCrudFactory(
        model=VisibilityType,
        update_schema=VisibilityTypeUpdate,
        create_schema=VisibilityTypeCreate,
        get_schema=VisibilityTypeGet
    )
):
    pass
