from src.schemas.system_schemas import (_UserCreate, _UserUpdate, _UserGet,
                                        _UserDeviceCreate, _UserDeviceUpdate, _UserDeviceGet,
                                        _MediaCreate, _MediaUpdate, _MediaGet,
                                        _VerificationCodeCreate, _VerificationCodeUpdate, _VerificationCodeGet,
                                        _TokenCreate, _TokenUpdate, _TokenGet,
                                        _DeviceProductCreate, _DeviceProductUpdate, _DeviceProductGet,
                                        _FavouriteContactCreate, _FavouriteContactUpdate, _FavouriteContactGet,
                                        _NotificationCreate, _NotificationUpdate, _NotificationGet,
                                        _VisibilityTypeCreate, _VisibilityTypeUpdate, _VisibilityTypeGet,
                                        _EventCreate, _EventUpdate, _EventGet,
                                        _ObserverCreate, _ObserverUpdate, _ObserverGet,
                                        _PassportCreate,_PassportUpdate,_PassportGet)


class UserModels:
    class Create(_UserCreate):
        pass

    class Update(_UserUpdate):
        pass

    class Get(_UserGet):
        pass


class UserDeviceModels:
    class Create(_UserDeviceCreate):
        pass

    class Update(_UserDeviceUpdate):
        pass

    class Get(_UserDeviceGet):
        pass


class MediaModels:
    class Create(_MediaCreate):
        pass

    class Update(_MediaUpdate):
        pass

    class Get(_MediaGet):
        pass


class VerificationCodeModels:
    class Create(_VerificationCodeCreate):
        pass

    class Update(_VerificationCodeUpdate):
        pass

    class Get(_VerificationCodeGet):
        pass


class TokenModels:
    class Create(_TokenCreate):
        pass

    class Update(_TokenUpdate):
        pass

    class Get(_TokenGet):
        pass


class DeviceProductModels:
    class Create(_DeviceProductCreate):
        pass

    class Update(_DeviceProductUpdate):
        pass

    class Get(_DeviceProductGet):
        pass


class FavouriteContactModels:
    class Create(_FavouriteContactCreate):
        pass

    class Update(_FavouriteContactUpdate):
        pass

    class Get(_FavouriteContactGet):
        pass


class NotificationModels:
    class Create(_NotificationCreate):
        pass

    class Update(_NotificationUpdate):
        pass

    class Get(_NotificationGet):
        pass


class VisibilityTypeModels:
    class Create(_VisibilityTypeCreate):
        pass

    class Update(_VisibilityTypeUpdate):
        pass

    class Get(_VisibilityTypeGet):
        pass


class EventModels:
    class Create(_EventCreate):
        pass

    class Update(_EventUpdate):
        pass

    class Get(_EventGet):
        pass


class ObserverModels:
    class Create(_ObserverCreate):
        pass

    class Update(_ObserverUpdate):
        pass

    class Get(_ObserverGet):
        pass


class PassportModels:
    class Create(_PassportCreate):
        pass

    class Update(_PassportUpdate):
        pass

    class Get(_PassportGet):
        pass


__all__ = [
    "UserModels", "UserDeviceModels", "MediaModels", "VerificationCodeModels",
    "TokenModels", "DeviceProductModels", "FavouriteContactModels", "NotificationModels",
    "VisibilityTypeModels", "EventModels", "ObserverModels", "PassportModels"
]
