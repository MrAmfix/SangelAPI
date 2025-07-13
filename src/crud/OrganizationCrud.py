from src.crud.base.factory import BaseCrudFactory
from src.models import Organization
from src.schemas import OrganizationModels


class OrganizationCrud(
    BaseCrudFactory(
        model=Organization,
        update_schema=OrganizationModels.Update,
        create_schema=OrganizationModels.Create,
        get_schema=OrganizationModels.Get
    )
):
    pass
