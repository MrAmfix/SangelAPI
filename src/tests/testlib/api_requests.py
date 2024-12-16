import requests


host = "http://localhost:8000"


def send_sms_api_request(phone):
    payload = {"phone": phone}
    response = requests.post(url=f"{host}/api/auth/send_code", json=payload)
    return response


def get_code_api_request(payload):
    response = requests.post(url=f"{host}/api/auth/check_code", json=payload)
    return response


def registration_api_request(user):
    response = requests.post(url=f"{host}/api/auth/registration",json=user)
    return response


def get_access_api_request(token):
    response = requests.post(url=f"{host}/api/auth/get_access", data=f'"{token}"')
    return response
