from src.crud.base.factory import BaseCrudFactory
from src.models.Token import Token
from src.schemas.system_schemas import TokenGet, TokenUpdate, TokenCreate


class TokenCrud(
    BaseCrudFactory(
        model=Token,
        update_schema=TokenUpdate,
        create_schema=TokenCreate,
        get_schema=TokenGet
    )
):
    pass
