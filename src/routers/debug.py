from fastapi import Depends, APIRouter, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from src.database import get_session
from src.models import VisibilityType
from src.settings import DEBUG_SECRET_KEY
from src.utils.enums import DefaultVisibilityType
from src.utils.loggers import api_logs

debug = APIRouter(prefix='/debug')


@api_logs(debug.post('/db_init_vis_type', include_in_schema=False))
async def db_init_visibility_type(
        key: str = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
):
    if key != DEBUG_SECRET_KEY:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Запрещено'
        )

    try:
        for en in DefaultVisibilityType:
            session.add(VisibilityType(name=en))
            await session.commit()
        return {'detail': 'Выполнено'}
    except Exception as _ex:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_ex)
        )
