from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.helpers.utils import get_token_data, credentials_exception
from src.crud.UserCrud import UserCrud
from src.database import get_session


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=""auth/login"")
security = HTTPBearer()

async def access_token_auth(
        # token: str = Depends(oauth2_scheme),
        token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        session: AsyncSession = Depends(get_session)
):  
    
    payload = get_token_data(token.credentials)
    user_id = payload.get('user_id')
    if user_id is None:
        raise credentials_exception
    user = await UserCrud.get_by_id(session=session, record_id=user_id)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        'user': user,
        'payload': payload,
        'token': token.credentials
    }
