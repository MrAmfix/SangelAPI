from typing import Optional

from fastapi import APIRouter, Depends, Body
from pydantic.v1 import NoneBytes
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from src.auth.auth import access_token_auth
from src.crud import UserCrud, VisibilityTypeCrud
from src.database import get_session
from src.utils.enums import DefaultVisibilityType
from src.utils.loggers import api_logs


settings = APIRouter(prefix='/settings')


@settings.post('/set_visibility_type')
@api_logs
async def set_visibility_type_handler(
        auth_data: dict = Depends(access_token_auth),
        visibility_type: DefaultVisibilityType = Body(...),
        session: AsyncSession = Depends(get_session)
):
    user_id = auth_data['user'].id
    visibility_type_id = await VisibilityTypeCrud.get_by_enum(enum=visibility_type, session=session)

    try:
        await UserCrud.update(
            visibility_type_id=visibility_type_id,
            session=session,
            record_id=user_id
        )

        return {'detail': 'Тип установлен'}
    except IntegrityError as _ie:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Неправильный формат аргументов'
        )
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )

@settings.post('/edit_account')
@api_logs
async def edit_account_handler(
        auth_data: dict = Depends(access_token_auth),
        name: Optional[str] = Body(None),
        surname: Optional[str] = Body(None),
        patronymic: Optional[str] = Body(None),
        session: AsyncSession = Depends(get_session)
):
    if name is None and surname is None and patronymic is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Нужен хотя бы один параметр для изменения'
        )

    user_id = auth_data['user'].id
    try:
        await UserCrud.update(
            session=session,
            record_id=user_id,
            name=name,
            surname=surname,
            patronymic=patronymic
        )
        return {'detail': 'Изменения прошли успешно'}

    except IntegrityError as _ie:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Неправильный формат аргументов'
        )
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )