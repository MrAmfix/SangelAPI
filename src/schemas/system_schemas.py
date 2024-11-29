from datetime import datetime
from typing import List, Optional
from pydantic import Field, BaseModel, ConfigDict, UUID4
from src.schemas.cropped_schemas import (_MediaCrop, _VisibilityTypeCrop,
                                         _TokenCrop, _NotificationCrop,
                                         _DeviceProductCrop, _UserDeviceCrop,
                                         _FavouriteContactCrop, _UserCrop,
                                         _EventCrop, _ObserverCrop)


class _UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    surname: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    patronymic: Optional[str] = Field(None, max_length=30, pattern=r'^[А-Яа-я-]+$')
    phone: str = Field(pattern=r'^\+7\d{10}$|^8\d{10}$')
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    city: str = Field(max_length=50)
    is_active: bool = True

    photo_id: Optional[UUID4] = None
    visibility_type_id: UUID4


class _UserUpdate(_UserCreate):
    id: UUID4


class _UserGet(_UserUpdate):
    photo: Optional["_MediaCrop"] = None
    visibility_type: "_VisibilityTypeCrop"
    tokens: List["_TokenCrop"]
    devices: List["_UserDeviceInUser"]
    favourite_contacts: List["_FavouriteContactInUser"]
    linked_contacts: List["_FavouriteContactInUser"]
    notifications: List["_NotificationCrop"]
    events: List["_EventInUser"]
    observers: List["_ObserverInUser"]

    created_at: datetime
    updated_at: datetime

    """
        Далее - классы-расширения от обрезанных моделей
    """

    class _UserDeviceInUser(_UserDeviceCrop):
        device: "_DeviceProductCrop"

    class _FavouriteContactInUser(_FavouriteContactCrop):
        owner: "_UserCrop"
        linked_user: Optional["_UserCrop"] = None

    class _EventInUser(_EventCrop):
        observers: List["_ObserverCrop"]
        pass

    class _ObserverInUser(_ObserverCrop):
        event: "_EventCrop"


class _UserDeviceCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID4
    device_id: UUID4


class _UserDeviceUpdate(_UserDeviceCreate):
    id: UUID4


class _UserDeviceGet(_UserDeviceUpdate):
    user: "_UserCrop"
    device: "_DeviceProductCrop"

    created_at: datetime


class _MediaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    media_link: str = Field(max_length=255)
    is_photo: bool

    user_id: Optional[UUID4]


class _MediaUpdate(_MediaCreate):
    id: UUID4


class _MediaGet(_MediaUpdate):
    user: "_UserCrop"

    created_at: datetime
    updated_at: datetime


class _VerificationCodeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str = Field(max_length=6, pattern=r'^\d{6}$')
    phone: str = Field(pattern=r'^\+7\d{10}$|^8\d{10}$')


class _VerificationCodeUpdate(_VerificationCodeCreate):
    pass


class _VerificationCodeGet(_VerificationCodeUpdate):
    created_at: datetime


class _TokenCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    refresh_token: str

    user_id: UUID4


class _TokenUpdate(_TokenCreate):
    id: UUID4


class _TokenGet(_TokenUpdate):
    user: "_UserCrop"

    created_at: datetime


class _DeviceProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    mac_address: str = Field(max_length=50)
    description: Optional[str] = None


class _DeviceProductUpdate(_DeviceProductCreate):
    id: UUID4


class _DeviceProductGet(_DeviceProductUpdate):
    users: List["_UserDeviceInDeviceProduct"]

    created_at: datetime

    class _UserDeviceInDeviceProduct(_UserDeviceCrop):
        user: "_UserCrop"


class _FavouriteContactCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    phone: str = Field(pattern=r'^\+7\d{10}$|^8\d{10}$')

    owner_id: UUID4
    linked_user_id: Optional[UUID4] = None


class _FavouriteContactUpdate(_FavouriteContactCreate):
    id: UUID4


class _FavouriteContactGet(_FavouriteContactUpdate):
    owner: "_UserCrop"
    linked_user: Optional["_UserCrop"] = None

    created_at: datetime


class _NotificationCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    body: str

    user_id: UUID4


class _NotificationUpdate(_NotificationCreate):
    id: UUID4


class _NotificationGet(_NotificationUpdate):
    user: "_UserCrop"

    created_at: datetime


class _VisibilityTypeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=50)


class _VisibilityTypeUpdate(_VisibilityTypeCreate):
    id: UUID4


class _VisibilityTypeGet(_VisibilityTypeUpdate):
    users: List["_UserCrop"]


class _EventCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    start_latitude: float
    start_longitude: float
    is_active: bool = True

    user_id: UUID4


class _EventUpdate(_EventCreate):
    id: UUID4
    complete_date: Optional[datetime] = None


class _EventGet(_EventUpdate):
    user: "_UserCrop"
    observers: List["_ObserverInEvent"]

    created_at: datetime

    class _ObserverInEvent(_ObserverCrop):
        user: "_UserCrop"


class _ObserverCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID4
    event_id: UUID4


class _ObserverUpdate(_ObserverCreate):
    id: UUID4


class _ObserverGet(_ObserverUpdate):
    user: "_UserCrop"
    event: "_EventCrop"

    created_at: datetime
