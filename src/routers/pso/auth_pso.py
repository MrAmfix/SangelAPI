from uuid import UUID
from typing import Optional, List
from datetime import timedelta
from fastapi import APIRouter, Depends, Body, File, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_429_TOO_MANY_REQUESTS, HTTP_403_FORBIDDEN

from src.auth.helpers.utils import (
    create_access_token,
    create_refresh_token,
    get_checked_token_data
)
from src.crud import (
    UserCrud,
    VerificationCodeCrud,
    TokenCrud,
    RegistrationTokenCrud,
    OrganizationCrud,
    EmployeeCrud
)
from src.database import get_session
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from src.utils.formatters import normalize_phone
from src.utils.loggers import api_logs
from src.utils.moscow_datetime import datetime_now_moscow
from src.utils.sms import check_expired_code, generate_code, send_sms


pso = APIRouter(prefix='/auth/pso')


@api_logs(pso.post('/send_code'))
async def send_code_handler(
    phone: str = Depends(normalize_phone),
    session: AsyncSession = Depends(get_session)
):
    try:
        last_code = await VerificationCodeCrud.get_last_code(phone=phone, session=session)
        if last_code is not None and not check_expired_code(last_code.created_at):
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Код уже был отправлен ранее, повторная отправка возможна раз в {VERIFICATION_CODE_EXPIRE_SECONDS} секунд"
            )
        code = generate_code()
        sms_response = await send_sms(destination=phone[1:], code=code)
        if sms_response.status != 200:
            raise HTTPException(status_code=sms_response.status, detail="Ошибка отправки кода")
        await VerificationCodeCrud.create(session=session, code=code, phone=phone)
        return {"detail": "Код отправлен"}
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Ошибка отправки кода')


@api_logs(pso.post('/check_code'))
async def check_code_handler(
    phone: str = Depends(normalize_phone),
    code: str = Body(...),
    session: AsyncSession = Depends(get_session)
):
    verification_code = await VerificationCodeCrud.get_last_code(session=session, phone=phone)
    if verification_code is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Номер не найден')
    if check_expired_code(verification_code.created_at):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Код истек')
    if verification_code.code != code:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Неверный код')
    user = await UserCrud.get_filtered_by_params(session=session, phone=phone)
    if user:
        access_token = create_access_token(data={'user_id': str(user[0].id)})
        refresh_token = create_refresh_token(data={'user_id': str(user[0].id)})
        await TokenCrud.create(session=session, refresh_token=refresh_token, user_id=user[0].id)
        return {"detail": "Код верен", "is_authorized": True, "access_token": access_token, "refresh_token": refresh_token}
    reg_token = await RegistrationTokenCrud.create(session=session, phone=phone)
    return {"detail": "Код верен", "is_authorized": False, "registration_token": reg_token.id}


@api_logs(pso.post('/create_organization'))
async def create_organization_handler(
    name: str = Body(...),
    contact_name: str = Body(...),
    phone: str = Depends(normalize_phone),
    email: str = Body(...),
    legal_address: str = Body(...),
    license_scan: UploadFile = File(...),
    logo: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        org = await OrganizationCrud.create(
            session=session,
            name=name,
            contact_name=contact_name,
            phone=phone,
            email=email,
            legal_address=legal_address,
            license_scan=license_scan,
            logo=logo
        )
        return {"detail": "Организация зарегистрирована", "admin_token": org.admin_token}
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Организация уже существует')


@api_logs(pso.post('/register_employee'))
async def register_employee_handler(
    registration_token: UUID = Body(...),
    name: str = Body(...),
    surname: str = Body(...),
    patronymic: Optional[str] = Body(None),
    phone: str = Depends(normalize_phone),
    organization_code: str = Body(...),
    session: AsyncSession = Depends(get_session)
):
    reg = await RegistrationTokenCrud.get_by_id(session=session, record_id=registration_token)
    if not reg or reg.created_at + timedelta(minutes=15) < datetime_now_moscow():
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Запрещено!')
    try:
        emp = await EmployeeCrud.create(
            session=session,
            registration_token=registration_token,
            name=name,
            surname=surname,
            patronymic=patronymic,
            phone=phone,
            organization_code=organization_code
        )
        access_token = create_access_token(data={'user_id': str(emp.id)})
        refresh_token = create_refresh_token(data={'user_id': str(emp.id)})
        await TokenCrud.create(session=session, refresh_token=refresh_token, user_id=emp.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Ошибка регистрации / Пользователь уже существует')


@api_logs(pso.post('/get_access'))
async def get_access_handler(
    refresh_token: str = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
):
    try:
        payload = await get_checked_token_data(token=refresh_token, session=session, refresh=True)
        if not payload:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Неверный токен')
        access_token = create_access_token(data={'user_id': str(payload['user_id'])})
        new_refresh = create_refresh_token(data={'user_id': str(payload['user_id'])})
        await TokenCrud.create(session=session, refresh_token=new_refresh, user_id=payload['user_id'])
        return {"access_token": access_token, "refresh_token": new_refresh}
    except HTTPException as he:
        raise HTTPException(status_code=he.status_code, detail='Токен истек')


@api_logs(pso.get('/requests'))
async def get_requests_handler(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    reqs = await RequestCrud.get_pending(session=session)
    return [{"id": r.id, "name": r.name, "phone": r.phone, "role": r.role} for r in reqs]


@api_logs(pso.post('/approve_request'))
async def approve_request_handler(
    current_user=Depends(get_current_user),
    request_id: UUID = Body(...),
    approved: bool = Body(...),
    session: AsyncSession = Depends(get_session)
):
    await RequestCrud.process(session=session, request_id=request_id, approved=approved)
    return {"detail": "Заявка обработана"}
