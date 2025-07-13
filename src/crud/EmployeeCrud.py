from src.crud.base.factory import BaseCrudFactory
from src.models import Employee
from src.schemas import EmployeeModels


class EmployeeCrud(
    BaseCrudFactory(
        model=Employee,
        update_schema=EmployeeModels.Update,
        create_schema=EmployeeModels.Create,
        get_schema=EmployeeModels.Get
    )
):
    pass
