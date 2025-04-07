from datetime import datetime, timedelta
from random import randint
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from src.utils.moscow_datetime import set_moscow_timezone, datetime_now_moscow
import aiohttp
from src.settings import SMS_API_PHONE_NUMBER, SMS_API_VERIFICATION_TOKEN


def generate_code():
    return str(randint(1000000, 9999999))[1:]


def check_expired_code(created_date: datetime):
    """
    True - код истек
    False - код еще действует
    """

    return (set_moscow_timezone(created_date) < datetime_now_moscow()
            - timedelta(seconds=int(VERIFICATION_CODE_EXPIRE_SECONDS)))


async def send_sms(destination: str, code: str):

    url = "https://api.exolve.ru/messaging/v1/SendSMS"
    headers = {
        "Authorization": f"Bearer {SMS_API_VERIFICATION_TOKEN}"
    }
    data = {
        "number": SMS_API_PHONE_NUMBER,
        "destination": destination,
        "text": code,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, headers=headers, json=data) as response:
                return response
        except Exception as e:
            raise Exception(f"Произошла ошибка: {e}")
