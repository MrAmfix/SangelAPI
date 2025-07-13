from src.crud.base.factory import BaseCrudFactory
from src.models import SecurityGroup
from src.schemas import SecurityGroupModels


class SecurityGroupCrud(
    BaseCrudFactory(
        model=SecurityGroup,
        update_schema=SecurityGroupModels.Update,
        create_schema=SecurityGroupModels.Create,
        get_schema=SecurityGroupModels.Get
    )
):
    pass
