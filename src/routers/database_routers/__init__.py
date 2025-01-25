from uuid import UUID
from fastapi import Depends, APIRouter, Body, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST
from src.auth.auth import access_token_auth
from src.crud.base.factory import CrudFactory
from src.database import get_session
from src.utils.loggers import api_logs


def create_all_routers(
        prefix: str,
        crud: type(CrudFactory)
) -> APIRouter:
    router = APIRouter(prefix=prefix)

    @router.post('/create')
    @api_logs
    async def th_create(
            auth_data: dict = Depends(access_token_auth),
            data: crud.create_schema = Body(...),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            return await crud.create(session=session, **data.model_dump())
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    @router.put('/update')
    @api_logs
    async def th_update(
            auth_data: dict = Depends(access_token_auth),
            data: crud.update_schema = Body(...),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            return await crud.update(session=session, record_id=data.id, **data.model_dump())
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    @router.delete('/delete')
    @api_logs
    async def th_delete(
            auth_data: dict = Depends(access_token_auth),
            record_id: UUID = Body(...),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            return await crud.delete(session=session, record_id=record_id)
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    @router.get('/get')
    @api_logs
    async def th_get(
            record_id: UUID = Query(...),
            auth_data: dict = Depends(access_token_auth),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            return await crud.get_by_id(session=session, record_id=record_id)
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    @router.get('/get_all')
    @api_logs
    async def th_get_all(
            offset: int = Query(0),
            limit: int = Query(100),
            auth_data: dict = Depends(access_token_auth),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            return await crud.get_all(session=session, offset=offset, limit=limit)
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    @router.get('/get_filtered_by_params')
    @api_logs
    async def th_get_filtered_by_params(
            params: crud.get_schema = Query(...),
            auth_data: dict = Depends(access_token_auth),
            session: AsyncSession = Depends(get_session)
    ):
        try:
            clean_params = {key: value for key, value in params.model_dump().items() if value is not None}
            return await crud.get_filtered_by_params(session=session, **clean_params)
        except Exception as _e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(_e))

    return router
