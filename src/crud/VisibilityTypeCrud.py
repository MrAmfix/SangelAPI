from src.crud.base.factory import BaseCrudFactory
from src.models import VisibilityType
from src.schemas import VisibilityTypeModels


class VisibilityTypeCrud(
    BaseCrudFactory(
        model=VisibilityType,
        update_schema=VisibilityTypeModels.Update,
        create_schema=VisibilityTypeModels.Create,
        get_schema=VisibilityTypeModels.Get
    )
):
    pass
