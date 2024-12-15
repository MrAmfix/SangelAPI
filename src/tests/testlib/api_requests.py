import requests


host = "http://localhost:8000"



def send_sms_api_request(phone):
    payload = {"phone" : phone}
    response = requests.post(url=f"{host}/auth/send_code",json=payload)
    return response

def get_code_api_request(payload):

    response = requests.post(url=f"{host}/auth/check_code",json=payload)
    return response

def reqistration_api_request(user):
    response = requests.post(url=f"{host}/auth/registration",json=user)
    return response

def get_acsess_api_request(token):
    print(token)
    response = requests.post(url=f"{host}/auth/get_access",json=token)
    return response
