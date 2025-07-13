from src.crud.base.factory import BaseCrudFactory
from src.models import EmployeeRole
from src.schemas import EmployeeRoleModels


class EmployeeRoleCrud(
    BaseCrudFactory(
        model=EmployeeRole,
        update_schema=EmployeeRoleModels.Update,
        create_schema=EmployeeRoleModels.Create,
        get_schema=EmployeeRoleModels.Get
    )
):
    pass
