from src.crud.base.factory import BaseCrudFactory
from src.models import Token
from src.schemas import TokenModels


class TokenCrud(
    BaseCrudFactory(
        model=Token,
        update_schema=TokenModels.Update,
        create_schema=TokenModels.Create,
        get_schema=TokenModels.Get
    )
):
    pass
