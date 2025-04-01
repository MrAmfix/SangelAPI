from typing import Optional
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from src.crud.PassportCrud import PassportCrud
from src.crud.UserCrud import UserCrud
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import access_token_auth
from src.utils.loggers import api_logs



passport = APIRouter(prefix="/passport")
get_passport = APIRouter(prefix="/get_passport")

@api_logs(passport.post(""))
async def add_passport_data(
    name: str,
    surname: str,
    patronymic: Optional[str],
    passport_series: str,
    passport_number: str,
    passport_agency: str,
    passport_code: str,
    passport_address: str,
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session)
    ):
    try:

        user_data = await UserCrud.get_by_id(
            session=session,
            record_id=auth_data["user"].id
        )

        if user_data.passport_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Паспортные данные уже внесены")
        
        passport_query = await PassportCrud.create(
            session=session,
            name=name,
            surname=surname,
            patronymic=patronymic,
            passport_series= passport_series,
            passport_number=passport_number,
            passport_agency=passport_agency,
            passport_code=passport_code,
            passport_address=passport_address,
        )
        
        await UserCrud.update(
            session=session,
            record_id=auth_data["user"].id,
            passport_id=passport_query.id              
        )

        return {
            "code": status.HTTP_200_OK,
            "detail": "OK"
            }
    except ValidationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Неверный формат данных ")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Ошибка: {str(e)}")


@api_logs(get_passport.get(""))
async def get_passport_data(
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session)
    ):
    try:
        user_data = await UserCrud.get_by_id(
            session=session,
            record_id=auth_data["user"].id
        )

        if not user_data.passport_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Данные не найдены")
        
        passport_data = await PassportCrud.get_by_id(
            session=session,
            record_id=user_data.passport_id
        )

        return {
            "code": status.HTTP_200_OK,
            "detail": "OK",
            "passport": passport_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Ошибка: {str(e)}")