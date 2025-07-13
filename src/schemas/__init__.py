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
                                        _ObserverCreate, _ObserverUpdate, _ObserverGet, _RegistrationTokenCreate,
                                        _RegistrationTokenUpdate, _RegistrationTokenGet, _PassportCreate,
                                        _PassportUpdate, _PassportGet,
                                        _CardCreate, _CardUpdate, _CardGet, _OrganizationCreate, _OrganizationUpdate,
                                        _OrganizationGet, _EmployeeCreate, _EmployeeUpdate, _EmployeeGet,
                                        _EmployeeRoleCreate, _EmployeeRoleUpdate, _EmployeeRoleGet,
                                        _SecurityGroupCreate, _SecurityGroupUpdate, _SecurityGroupGet)


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


class RegistrationTokenModels:
    class Create(_RegistrationTokenCreate):
        pass

    class Update(_RegistrationTokenUpdate):
        pass

    class Get(_RegistrationTokenGet):
        pass


class PassportModels:
    class Create(_PassportCreate):
        pass

    class Update(_PassportUpdate):
        pass

    class Get(_PassportGet):
        pass


class CardModels:
    class Create(_CardCreate):
        pass

    class Update(_CardUpdate):
        pass

    class Get(_CardGet):
        pass


class OrganizationModels:
    class Create(_OrganizationCreate):
        pass

    class Update(_OrganizationUpdate):
        pass

    class Get(_OrganizationGet):
        pass


class EmployeeModels:
    class Create(_EmployeeCreate):
        pass

    class Update(_EmployeeUpdate):
        pass

    class Get(_EmployeeGet):
        pass


class EmployeeRoleModels:
    class Create(_EmployeeRoleCreate):
        pass

    class Update(_EmployeeRoleUpdate):
        pass

    class Get(_EmployeeRoleGet):
        pass


class SecurityGroupModels:
    class Create(_SecurityGroupCreate):
        pass

    class Update(_SecurityGroupUpdate):
        pass

    class Get(_SecurityGroupGet):
        pass


__all__ = [
    "UserModels", "UserDeviceModels", "MediaModels", "VerificationCodeModels",
    "TokenModels", "DeviceProductModels", "FavouriteContactModels", "NotificationModels",
    "VisibilityTypeModels", "EventModels", "ObserverModels", "RegistrationTokenModels",
    "PassportModels", "CardModels", "OrganizationModels", "EmployeeModels", "EmployeeRoleModels",
    "SecurityGroupModels"
]

