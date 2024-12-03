from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, UUID4


"""
    CroppedSchemas - обрезанные модели,
    используются для устранения бесконечных вложений,
    так же могут использоваться, как базовые модели для расширений в других моделях.
"""


class _UserCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    name: str
    surname: str
    patronymic: Optional[str] = None
    phone: str
    email: Optional[str] = None
    is_active: bool

    photo_id: Optional[UUID4] = None
    visibility_type_id: UUID4

    created_at: datetime
    updated_at: datetime


class _MediaCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    media_link: str
    is_photo: bool

    created_at: datetime
    updated_at: datetime


class _TokenCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    refresh_token: str

    user_id: UUID4

    created_at: datetime


class _DeviceProductCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    mac_address: str
    description: Optional[str] = None

    created_at: datetime


class _UserDeviceCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4

    user_id: UUID4
    device_id: UUID4

    created_at: datetime


class _FavouriteContactCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    name: str
    phone: str

    owner_id: UUID4
    linked_user_id: Optional[UUID4] = None

    created_at: datetime


class _NotificationCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    title: str
    body: str

    user_id: UUID4

    created_at: datetime


class _VisibilityTypeCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    name: str


class _EventCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4
    start_latitude: float
    start_longitude: float
    is_active: bool
    complete_date: Optional[datetime] = None

    user_id: UUID4
    # security_group_id: Optional[UUID4] = None

    created_at: datetime


class _ObserverCrop(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID4

    user_id: UUID4
    event_id: UUID4

    created_at: datetime
