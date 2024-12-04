from random import randint
import requests
from settings import SMS_API_URL,SMS_API_KEY,SMS_API_NUMBER
import asyncio
import aiohttp

def generate_code():
    return str(randint(100000, 999999))


async def send_sms(user_number,message):

    url = SMS_API_URL

    headers = {

        "Authorization": SMS_API_KEY
    }

    data = {
        "number": SMS_API_NUMBER,
        "destination": user_number,
        "text" :message,
    }

    with aiohttp.ClientSession() as session:
        async with session.post(url=url,headers=headers,json=data) as response:
            return response.status_code
        


        

    
    
