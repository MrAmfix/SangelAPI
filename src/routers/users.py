from fastapi import Depends,HTTPException, status
from fastapi import APIRouter
from src.crud.UserCrud import UserCrud
from src.crud.EventCrud import EventCrud
from src.schemas.cropped_schemas import _UserCrop
from src.crud.ObserverCrud import ObserverCrud
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import access_token_auth
from src.utils.loggers import api_logs


users = APIRouter(prefix="/user")


@api_logs(users.get("/get_info"))
async def get_user_info(
    auth_data: dict = Depends(access_token_auth),
    session: AsyncSession = Depends(get_session),
):  
    try:

        cropped_user_response = _UserCrop.model_validate(auth_data['user'])

        active_event_response = await EventCrud.get_filtered_by_params(
            session=session, 
            user_id=auth_data['user'].id,
            is_active=True
            )
        
        active_observer_events_response = await ObserverCrud.get_filtered_by_active_events_observer(
            session=session, 
            user_id=auth_data['user'].id,       
            )
        
        return {
            "user":cropped_user_response.model_dump(),
            "is_active_event": True if active_event_response else False,
            "active_observer_events": active_observer_events_response,
            }

    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(_e)}"
        )
