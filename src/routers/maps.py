import uuid

from charset_normalizer.utils import is_accentuated
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from src.auth.auth import access_token_auth
from src.crud import EventCrud, ObserverCrud
from src.database import get_session
from src.utils.loggers import api_logs
from src.utils.maps import distance


maps = APIRouter(prefix='/maps')


@api_logs(maps.post('/send_location'))
async def send_location(
    auth_data: dict = Depends(access_token_auth),
    latitude: float = Body(...),
    longitude: float = Body(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        current_event = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True
        )

        if not current_event:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='У вас нет активных событий'
            )

        await EventCrud.update(
            session=session,
            record_id=current_event[0].id,
            current_latitude=latitude,
            current_longitude=longitude
        )

        return {'detail': 'Ok'}
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )


@api_logs(maps.get('/observe_help'))
async def observe_help(
    auth_data: dict = Depends(access_token_auth),
    latitude: float = Body(...),
    longitude: float = Body(...),
    session: AsyncSession = Depends(get_session)
):
    try:
        active_user_events = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True
        )
        if active_user_events:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='У вас есть активное событие, доступ к этой функции ограничен'
            )

        active_events = await EventCrud.get_filtered_by_params(
            session=session,
            is_active=True
        )

        nearby_events = []

        for event in active_events:
            if distance(latitude, longitude, event.current_latitude, event.current_longitude) <= 1500:
                nearby_events.append(event.id)

        return {'events_id': nearby_events}
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )


@api_logs(maps.get('/get_event_status'))
async def get_event_status(
    auth_data: dict = Depends(access_token_auth),
    event_id: uuid.UUID = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
):
    try:
        event = await EventCrud.get_by_id(
            session=session,
            record_id=event_id
        )

        if not event:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='События с таким ID не существует'
            )

        return {
            'status': ('ACTIVE' if event.is_active else 'ENDED'),
            'latitude': event.current_latitude,
            'longitude': event.current_longitude
        }
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )


@api_logs(maps.post('/join_event'))
async def join_event(
    auth_data: dict = Depends(access_token_auth),
    event_id: uuid.UUID = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
):
    try:
        active_user_events = await EventCrud.get_filtered_by_params(
            session=session,
            user_id=auth_data['user'].id,
            is_active=True
        )
        if active_user_events:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='У вас есть активное событие, доступ к этой функции ограничен'
            )

        event = await EventCrud.get_filtered_by_params(
            session=session,
            id=event_id,
            is_active=True
        )
        observer = await ObserverCrud.get_filtered_by_params(
            session=session,
            event_id=event_id,
            user_id=auth_data['user'].id
        )

        if not event:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='События с таким ID не существует / событие не активно'
            )
        if event and observer:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Вы уже являетесь наблюдателем события'
            )

        await ObserverCrud.create(
            session=session,
            event_id=event_id,
            user_id=auth_data['user'].id
        )
        return {'detail': 'Ok'}
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )


@api_logs(maps.post('/leave_event'))
async def leave_event(
    auth_data: dict = Depends(access_token_auth),
    event_id: uuid.UUID = Body(..., embed=True),
    session: AsyncSession = Depends(get_session)
):
    try:
        event = await EventCrud.get_filtered_by_params(
            session=session,
            id=event_id,
            is_active=True
        )
        observer = await ObserverCrud.get_filtered_by_params(
            session=session,
            event_id=event_id,
            user_id=auth_data['user'].id
        )

        if not event:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'События с таким ID не существует / закончилось'
            )
        if not observer:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Вы не являетесь наблюдателем этого события'
            )

        await ObserverCrud.delete(session=session, record_id=observer[0].id)
        return {'detail': 'Ok'}
    except Exception as _e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )
