import jwt
from datetime import timedelta
from typing import Optional
from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.crud import UserCrud
from src.settings import (JWT_ALGORITHM, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
                          JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
from src.utils.moscow_datetime import datetime_now_moscow


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
) -> str:
    to_encode = data.copy()
    expire = datetime_now_moscow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(
        data: dict,
        expires_delta: Optional[timedelta] = timedelta(minutes=int(JWT_REFRESH_TOKEN_EXPIRE_MINUTES))
) -> str:
    to_encode = data.copy()
    expire = datetime_now_moscow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


def get_token_data(token: str) -> dict:
    payload = verify_token(token)
    if payload:
        return payload
    return {}


async def get_checked_token_data(token: str, session: AsyncSession) -> dict:
    payload = verify_token(token)
    if not payload or 'user_id' not in payload:
        return {}
    if not await UserCrud.get_by_id(session=session, record_id=payload['user_id']):
        return {}
    return payload
