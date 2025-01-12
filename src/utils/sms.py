from datetime import datetime, timedelta
from random import randint
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from src.utils.moscow_datetime import set_moscow_timezone, datetime_now_moscow


def generate_code():
    return str(randint(1000000, 9999999))[1:]


def check_expired_code(created_date: datetime):
    """
    True - код истек
    False - код еще действует
    """

    return (set_moscow_timezone(created_date) < datetime_now_moscow()
            - timedelta(seconds=int(VERIFICATION_CODE_EXPIRE_SECONDS)))
