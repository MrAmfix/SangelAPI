from datetime import datetime
from typing import List, Optional
from pydantic import Field, BaseModel, ConfigDict, UUID4, field_validator
from src.utils.encrypt import decrypt_data
from utils.moscow_datetime import datetime_now_moscow
from src.schemas.cropped_schemas import (_MediaCrop, _VisibilityTypeCrop,
                                         _TokenCrop, _NotificationCrop,
                                         _DeviceProductCrop, _UserDeviceCrop,
                                         _FavouriteContactCrop, _UserCrop,
                                         _EventCrop, _ObserverCrop, _PassportCrop)


class _UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    surname: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    patronymic: Optional[str] = Field(None, max_length=30, pattern=r'^[А-Яа-я-]+$')
    phone: str = Field(pattern=r'^\+7\d{10}$|^8\d{10}$')
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    is_active: bool = True

    photo_id: Optional[UUID4] = None
    passport_id: Optional[UUID4] = None
    card_id: Optional[UUID4] = None
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
    passports: Optional["_PassportCrop"] = None

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


class _MediaUpdate(_MediaCreate):
    id: UUID4


class _MediaGet(_MediaUpdate):
    user: Optional["_UserCrop"]

    created_at: datetime
    updated_at: datetime


class _VerificationCodeCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str = Field(max_length=6, pattern=r'^\d{6}$')
    phone: str = Field(pattern=r'^\+7\d{10}$|^8\d{10}$')


class _VerificationCodeUpdate(_VerificationCodeCreate):
    id: UUID4


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


class _PassportCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    surname: str = Field(max_length=30, pattern=r'^[А-Яа-я-]+$')
    patronymic: Optional[str] = Field(None, max_length=30, pattern=r'^[А-Яа-я-]+$')
    passport_series: str = Field(max_length=4, pattern=r'^\d{4}$')
    passport_number: str = Field(max_length=6, pattern=r'^\d{6}$')
    passport_agency: str = Field(max_length=200, pattern=r'^[А-Яа-яЁё\s\d,.-]+$')
    passport_code: str = Field(pattern=r'^\d{3}-\d{3}$')
    passport_address: str = Field(max_length=300, pattern=r'^[А-Яа-яЁё\s\d,.-]+$')



class _PassportUpdate(_PassportCreate):
    id: UUID4


class _PassportGet(_PassportUpdate):

    name: str
    surname: str
    patronymic: Optional[str]
    passport_series: str
    passport_number: str
    passport_agency: str
    passport_code: str
    passport_address: str

    created_at: datetime
    updated_at: datetime


    @field_validator(
            'name', 
            'surname', 
            'patronymic', 
            'passport_series', 
            'passport_number', 
            'passport_agency', 
            'passport_code', 
            'passport_address', 
            mode='before'
        )
    def decrypt_fields(cls, value):
        return decrypt_data(value)


class _RegistrationTokenCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    phone: str


class _RegistrationTokenUpdate(_RegistrationTokenCreate):
    id: UUID4


class _RegistrationTokenGet(_RegistrationTokenUpdate):
    created_at: datetime


class _CardCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    number: str = Field(pattern=r'^\d{16}$',description="Номер карты должен содержать 16 цифр")
    validity_period: str = Field(pattern=r'^\d{2}/\d{2}$', description="Формат ввода срока действия: мм/гг")
    cvv_number: str = Field(pattern=r'^\d{3}$', description="CVV должен содержать 3 цифры")

    @field_validator('validity_period')
    def check_validity_period(cls, v):
        exp_date = datetime.strptime(v, '%m/%y')
        if exp_date < datetime.now():
            raise ValueError('Срок действия карты истек')
        return v


class _CardUpdate(_CardCreate):
    id: UUID4


class _CardGet(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    number: str
    validity_period: str
    cvv_number: str

    created_at: datetime
    updated_at: datetime

    @field_validator(
            "number",
            "validity_period",
            "cvv_number",
            mode='before'
        )
    def decrypt_fields(cls, value):
        return decrypt_data(value)
