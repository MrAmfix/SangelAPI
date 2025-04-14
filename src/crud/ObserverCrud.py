from typing import List, Optional
from uuid import UUID
from src.crud.base.factory import BaseCrudFactory
from src.models import Observer, Event
from src.schemas import ObserverModels
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.base.factory import BaseCrudFactory


class ObserverCrud(
    BaseCrudFactory(
        model=Observer,
        update_schema=ObserverModels.Update,
        create_schema=ObserverModels.Create,
        get_schema=ObserverModels.Get
    )
):
    
    @staticmethod
    async def get_filtered_by_active_events_observer(
        session: AsyncSession, 
        user_id: UUID
        ) -> Optional[List[Observer]]:

        result = await session.execute(
            select(Observer.event_id).join(Observer.event)
            .where(Observer.user_id == user_id)
            .filter(Event.is_active == True)
        )

        return result.scalars().all()

