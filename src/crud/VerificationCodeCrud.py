from src.crud.base.factory import BaseCrudFactory
from src.models import VerificationCode
from src.schemas import VerificationCodeModels


class VerificationCodeCrud(
    BaseCrudFactory(
        model=VerificationCode,
        update_schema=VerificationCodeModels.Update,
        create_schema=VerificationCodeModels.Create,
        get_schema=VerificationCodeModels.Get
    )
):
    pass
