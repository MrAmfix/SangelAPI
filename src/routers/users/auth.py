from uuid import UUID
from typing import Optional
from datetime import timedelta
from fastapi import APIRouter, Depends, Body
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS, HTTP_403_FORBIDDEN
from src.auth.helpers.utils import create_access_token, create_refresh_token, get_checked_token_data
from src.crud import UserCrud, VisibilityTypeCrud, VerificationCodeCrud, TokenCrud
from src.crud.RegistrationToken import RegistrationTokenCrud
from src.database import get_session
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from src.utils.enums import DefaultVisibilityType
from src.utils.formatters import normalize_phone
from src.utils.loggers import api_logs
from src.utils.moscow_datetime import datetime_now_moscow
from src.utils.sms import check_expired_code, generate_code, send_sms


auth = APIRouter(prefix='/auth')


@api_logs(auth.post('/send_code'))
async def send_code_handler(
        phone: str = Depends(normalize_phone),
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
        phone_code = generate_code()
        cropped_phone_for_sms_api = phone[1:]

        sms_response = await send_sms(
            destination=cropped_phone_for_sms_api,
            code=phone_code
        )

        if not sms_response.status == 200:
            raise HTTPException(
                status_code=sms_response.status,
                detail="Ошибка отправки СМС"
            )
        
        await VerificationCodeCrud.create(
            session=session,
            code=phone_code,
            phone=phone
        )

        return {'detail': 'Код отправлен'}
    
    except IntegrityError as _ie:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='Неправильно указан номер телефона'
        )
    except HTTPException as _he:
        raise _he
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(auth.post('/check_code'))
async def check_code_handler(
        phone: str = Depends(normalize_phone),
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

    reg_token = await RegistrationTokenCrud.create(session=session, phone=phone)
    return {
        'detail': 'Код верен',
        'is_authorized': False,
        'registration_token': reg_token.id
    }


@api_logs(auth.post('/registration'))
async def registration_handler(
        registration_token: UUID = Body(...),
        name: str = Body(...),
        surname: str = Body(...),
        phone: str = Depends(normalize_phone),
        patronymic: Optional[str] = Body(None),
        email: Optional[str] = Body(None),
        session: AsyncSession = Depends(get_session)
):
    reg_token = await RegistrationTokenCrud.get_by_id(session=session, record_id=registration_token)
    if not reg_token or reg_token.created_at + timedelta(minutes=15) < datetime_now_moscow():
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Запрещено!'
        )
    try:
        user_by_phone = await UserCrud.get_filtered_by_params(
            session=session,
            phone=phone
        )
        user_by_email = await UserCrud.get_filtered_by_params(
            session=session,
            email=email
        )

        if user_by_phone:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Пользователь с таким телефоном уже существует'
            )
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Пользователь с такой почтой уже существует'
            )

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
    except IntegrityError as _ie:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'Данные введены в неправильном формате, {_ie}'
        )
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(auth.post('/get_access'))
async def get_access_handler(
        refresh_token: str = Body(..., embed=True),
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
