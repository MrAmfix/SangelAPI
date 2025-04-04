from typing import Optional
from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from src.auth.auth import access_token_auth
from src.crud import UserCrud, VisibilityTypeCrud, FavouriteContactCrud
from src.database import get_session
from src.routers.media import upload_image
from src.utils.enums import DefaultVisibilityType
from src.utils.loggers import api_logs
from pydantic import ValidationError
from src.crud.PassportCrud import PassportCrud
from src.crud.UserCrud import UserCrud



settings = APIRouter(prefix='/settings')


@api_logs(settings.post('/set_visibility_type'))
async def set_visibility_type_handler(
        auth_data: dict = Depends(access_token_auth),
        visibility_type: DefaultVisibilityType = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
):
    user_id = auth_data['user'].id
    visibility_type_id = (await VisibilityTypeCrud.get_by_enum(enum=visibility_type, session=session)).id

    try:
        await UserCrud.update(
            session=session,
            record_id=user_id,
            visibility_type_id=visibility_type_id
        )

        return {'detail': 'Тип установлен'}
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(settings.post('/edit_account'))
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

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(settings.delete('/del_favourite_contact'))
async def del_favourite_contact_handler(
        auth_data: dict = Depends(access_token_auth),
        phone: str = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
):
    user_id = auth_data['user'].id

    try:
        favourite_contact = await FavouriteContactCrud.get_filtered_by_params(
            session=session,
            owner_id=user_id,
            phone=phone
        )

        if not favourite_contact:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Этого избранного контакта не существует!"
            )

        request = await FavouriteContactCrud.delete(
            session=session,
            record_id=favourite_contact[0].id
        )

        return {'detail': 'Контакт удалён!'}

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(settings.post('/add_favourite_contact'))
async def add_favourite_contact_handler(
        auth_data: dict = Depends(access_token_auth),
        name: str = Body(...),
        phone: str = Body(...),
        session: AsyncSession = Depends(get_session)
):
    user_id = auth_data['user'].id

    try:
        favourite_contact = await FavouriteContactCrud.get_filtered_by_params(
            session=session,
            owner_id=user_id,
            phone=phone
        )

        if favourite_contact:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Такой контакт уже есть!"
            )

        linked_user = await UserCrud.get_filtered_by_params(
            session=session,
            phone=phone
        )

        new_favourite_contact = await FavouriteContactCrud.create(
            session=session,
            phone=phone,
            name=name,
            owner_id=user_id,
            linked_user_id=linked_user[0].id if linked_user else None
        )

        return {'detail': 'Контакт добавлен!'}

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@api_logs(settings.post('/edit_photo'))
async def edit_photo_handler(
        auth_data: dict = Depends(access_token_auth),
        photo: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
):
    await upload_image(
        auth_data=auth_data,
        file=photo,
        session=session
    )


@api_logs(settings.post("/passport"))
async def add_passport_data_handler(
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


@api_logs(settings.get("/get_passport"))
async def get_passport_data_handler(
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