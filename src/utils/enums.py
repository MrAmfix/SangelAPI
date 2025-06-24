from enum import Enum


class DefaultVisibilityType(str, Enum):
    ALL = 'Все'
    FAVOURITE_CONTACTS = 'Избранные контакты'
    NOBODY = 'Никто'


class AccountType(str, Enum):
    USER = 'USER'
    OWNER = 'OWNER'
    EMPLOYEE = 'EMPLOYEE'
    CAPTAIN_SSS = 'CAPTAIN_SSS'
    STAFF_SSS = 'STAFF_SSS'
