from enum import Enum


class DefaultVisibilityType(str, Enum):
    ALL = 'Все'
    FAVOURITE_CONTACTS = 'Избранные контакты'
    NOBODY = 'Никто'
