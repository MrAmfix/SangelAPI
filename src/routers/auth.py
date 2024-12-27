from typing import Optional
from fastapi import APIRouter, Depends, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS
from src.auth.helpers.utils import create_access_token, create_refresh_token, get_checked_token_data
from src.crud import UserCrud, VisibilityTypeCrud, VerificationCodeCrud, TokenCrud
from src.database import get_session
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from src.utils.enums import DefaultVisibilityType
from src.utils.sms import check_expired_code


auth = APIRouter(prefix='/auth')


@auth.post('/send_code')
async def send_code_handler(
        phone: str = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
):
    try:
        last_code = await VerificationCodeCrud.get_last_code(
            phone=phone,
            session=session
        )

        if last_code is not None and not check_expired_code(last_code.created_at):
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Код уже был отправлен ранее, повторная отправка возможна раз в "
                       f"{VERIFICATION_CODE_EXPIRE_SECONDS} секунд"
            )

        await VerificationCodeCrud.create(
            session=session,
            code='111111',
            phone=phone
        )

        return {'detail': 'Код отправлен'}
    except IntegrityError as _ie:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Неправильно указан номер телефона'
        )
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@auth.post('/check_code')
async def check_code_handler(
        phone: str = Body(...),
        code: str = Body(...),
        session: AsyncSession = Depends(get_session)
):
    verification_code = await VerificationCodeCrud.get_last_code(
        session=session,
        phone=phone
    )

    if verification_code is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Неверно указан номер телефона'
        )

    if check_expired_code(verification_code.created_at):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Код уже истек'
        )

    if verification_code.code != code:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Неправильный код'
        )

    user = await UserCrud.get_filtered_by_params(session=session, phone=phone)

    if user:
        access_token = create_access_token(data={'user_id': str(user[0].id)})
        refresh_token = create_refresh_token(data={'user_id': str(user[0].id)})
        await TokenCrud.create(
            session=session,
            refresh_token=refresh_token,
            user_id=user[0].id
        )
        return {
            'detail': 'Код верен',
            'is_authorized': True,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    return {
        'detail': 'Код верен',
        'is_authorized': False
    }


@auth.post('/registration')
async def registration_handler(
        name: str = Body(...),
        surname: str = Body(...),
        phone: str = Body(...),
        patronymic: Optional[str] = Body(None),
        email: Optional[str] = Body(None),
        session: AsyncSession = Depends(get_session)
):
    try:
        visibility_type = await VisibilityTypeCrud.get_by_enum(
            enum=DefaultVisibilityType.ALL,
            session=session
        )

        user = await UserCrud.create(
            session=session,
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
            email=email,
            visibility_type_id=visibility_type.id
        )

        access_token = create_access_token(data={'user_id': str(user.id)})
        refresh_token = create_refresh_token(data={'user_id': str(user.id)})
        await TokenCrud.create(
            session=session,
            refresh_token=refresh_token,
            user_id=user.id
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@auth.post('/get_access')
async def get_access_handler(
        refresh_token: str = Body(...),
        session: AsyncSession = Depends(get_session)
):
    try:
        payload = await get_checked_token_data(
            token=refresh_token,
            session=session,
            refresh=True
        )
        if not payload:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Неверный токен'
            )

        access_token = create_access_token(data={'user_id': str(payload['user_id'])})
        refresh_token = create_refresh_token(data={'user_id': str(payload['user_id'])})
        await TokenCrud.create(
            session=session,
            refresh_token=refresh_token,
            user_id=payload['user_id']
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    except HTTPException as _he:
        raise HTTPException(
            status_code=_he.status_code,
            detail=f'Токен истек, {_he}'
        )
    except Exception as _e:
        raise HTTPException(
            status_code=400,
            detail=str(_e)
        )
