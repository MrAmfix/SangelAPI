from typing import Optional
from fastapi import APIRouter, Depends, Body, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from src.auth.auth import access_token_auth
from src.crud import UserCrud, VisibilityTypeCrud, FavouriteContactCrud
from src.database import get_session
from src.routers.media import upload_image
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

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@settings.delete('/del_favourite_contact')
@api_logs
async def del_favourite_contact_handler(
        auth_data: dict = Depends(access_token_auth),
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

        if not favourite_contact:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Этого избранного контакта не существует!"
            )

        request = await FavouriteContactCrud.delete(
            session=session,
            record_id=favourite_contact.id
        )

        return {'detail': 'Контакт удалён!'}

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@settings.post('/add_favourite_contact')
@api_logs
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

        new_favourite_contact = await UserCrud.create(
            session=session,
            phone=phone,
            name=name,
            owner_id=user_id,
            linked_user_id=linked_user.id if linked_user else None
        )

        return {'detail': 'Контакт добавлен!'}

    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(_e)
        )


@settings.post('/edit_photo')
@api_logs
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
