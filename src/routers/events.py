from typing import Optional
from sqlalchemy.exc import DBAPIError
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from src.crud.EventCrud import EventCrud
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import access_token_auth
from src.utils.loggers import api_logs
from src.utils.moscow_datetime import datetime_now_moscow


events = APIRouter(prefix="/my_devices")


@api_logs(events.post("/new_event"))
async def create_event(
    start_latitude: float,
    start_longitude: float,
    called_security_group: Optional[bool] = False,
    called_users: Optional[bool] = False,
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session)
):  
    try:
        active_event = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True
        )
        
        if active_event:
            await EventCrud.update(
                session=session,
                record_id=active_event.id,
                called_security_group=called_security_group,
                called_users=called_users
            )

            return {
            "code": status.HTTP_200_OK,
            "detail": "Поля вызовов у активного события обновлены"
            }
        
        await EventCrud.create(
            session=session,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            current_latitude=start_latitude,
            current_longitude=start_longitude,
            user_id=auth_data['user'].id,
            called_security_group=called_security_group,
            called_users=called_users,
        )
        
        return {
            "code": status.HTTP_200_OK,
            "detail": "Событие создано"
        }
    
    except DBAPIError as _de:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пропущены аргументы: {str(_de)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(e)}"
        )


@api_logs(events.delete("/stop_event"))
async def delete_event(
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session)
):
    try:
        active_event = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True)
        
        if not active_event:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Активных событий нет'
            )

        await EventCrud.update(
            session=session,
            record_id=active_event[0].id,
            complete_date=datetime_now_moscow(),
            is_active=False)
        
        return {
            "code": status.HTTP_200_OK,
            "detail":'Событие удалено'
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(e)}"
        )


@api_logs(events.get("/get_event"))
async def get_event(
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session)
):
    try:
        event = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"Активных событий нет"
        )

        return {
            "code": status.HTTP_200_OK,
            "detail": "Активное событие существует",
            "event": event[0]
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(e)}"
        ) 


