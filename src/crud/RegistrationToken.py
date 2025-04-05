from src.crud.base.factory import BaseCrudFactory
from src.models import RegistrationToken
from src.schemas import RegistrationTokenModels


class RegistrationTokenCrud(
    BaseCrudFactory(
        model=RegistrationToken,
        update_schema=RegistrationTokenModels.Update,
        create_schema=RegistrationTokenModels.Create,
        get_schema=RegistrationTokenModels.Get
    )
):
    pass
