import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    phone: str
    password: str
    username: str
    name: str
    surname: str
    patronymic: Optional[str]


class UserUpdate(UserCreate):
    id: uuid.UUID
    disabled: bool


class UserGet(UserUpdate):
    pass


class DeviceProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mac_address: str
    description: Optional[str]
    comment: Optional[str]
    user_id: uuid.UUID
    active: Optional[bool] = True


class DeviceProductUpdate(DeviceProductCreate):
    id: uuid.UUID


class DeviceProductGet(DeviceProductUpdate):
    pass


class FavouriteListCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: uuid.UUID


class FavouriteListUpdate(FavouriteListCreate):
    id: uuid.UUID


class FavouriteListGet(FavouriteListUpdate):
    pass


class NotificationCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    body: str
    user_id: uuid.UUID


class NotificationUpdate(NotificationCreate):
    id: uuid.UUID


class NotificationGet(NotificationUpdate):
    pass


class PhotoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    photo_link: str
    user_id: uuid.UUID


class PhotoUpdate(PhotoCreate):
    id: uuid.UUID


class PhotoGet(PhotoUpdate):
    pass


class UserStatusCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class UserStatusUpdate(UserStatusCreate):
    id: uuid.UUID


class UserStatusGet(UserStatusUpdate):
    pass


class VisibilityTypeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class VisibilityTypeUpdate(VisibilityTypeCreate):
    id: uuid.UUID


class VisibilityTypeGet(VisibilityTypeUpdate):
    pass


class TokenCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    refresh_token: str
    user_id: uuid.UUID


class TokenUpdate(TokenCreate):
    id: uuid.UUID


class TokenGet(TokenUpdate):
    pass
