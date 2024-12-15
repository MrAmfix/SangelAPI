from time import sleep
from src.tests.testlib import api_requests
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS


def test_send_sms():

    payload = '+71234567890'

    response = api_requests.send_sms_api_request(phone=payload)
    response_json =  response.json()
    expected_message = 'Код отправлен'

    assert response.status_code ==  200
    assert response_json['detail'] == expected_message


    sleep(int(VERIFICATION_CODE_EXPIRE_SECONDS)+1)

    wrong_payload = '+71234567'
    response = api_requests.send_sms_api_request(phone=wrong_payload)
    response_json =  response.json()

    expected_message = 'Неправильно указан номер телефона'
    assert response.status_code ==  400
    assert response_json['detail'] == expected_message

    sleep(int(VERIFICATION_CODE_EXPIRE_SECONDS)-1)

    fast_payload = '+71234567890'

    response = api_requests.send_sms_api_request(phone=fast_payload)
    response_json =  response.json()

    expected_message = f'Код уже был отправлен ранее, повторная отправка возможна раз в {VERIFICATION_CODE_EXPIRE_SECONDS} секунд'
    assert response.status_code ==  429
    assert response_json['detail'] == expected_message




def test_check_sms():

    payload = '+71234567890'

    response = api_requests.send_sms_api_request(phone=payload)

    payload = {  
        "phone": "+71234567890",
        "code": "111111"
    }
    response = api_requests.get_code_api_request(payload=payload)
    response_json =  response.json()

    expected_message = 'Код верен'

    assert response.status_code ==  200
    assert response_json['detail'] == expected_message

    payload = {  
        "phone": "+71234567890",
        "code": "111112"
    }

    response = api_requests.get_code_api_request(payload=payload)
    response_json =  response.json()

    expected_message = 'Неправильный код'

    assert response.status_code ==  400
    assert response_json['detail'] == expected_message

    payload = {  
        "phone": "+71234567",
        "code": "111111"
    }
    response =api_requests.get_code_api_request(payload=payload)
    response_json =  response.json()

    expected_message = 'Неверно указан номер телефона'

    assert response.status_code ==  400
    assert response_json['detail'] == expected_message


def test_registration(create_test_user):

    response = api_requests.reqistration_api_request(user=create_test_user)
    assert response.status_code == 200


def test_get_acsess(create_test_user):

    response_from_registration = api_requests.reqistration_api_request(user=create_test_user)
    response_json = response_from_registration.json()
    refresh_token = response_json["refresh_token"]

    response_from_get_acsess = api_requests.get_acsess_api_request(token=refresh_token)

    assert response_from_get_acsess.status_code == 200

    wrong_refresh_token = "wrong_token_value"

    response_from_get_acsess_wrong = api_requests.get_acsess_api_request(token=wrong_refresh_token)
    response_from_get_acsess_wrong_json = response_from_get_acsess_wrong.json()   
    expected_message = 'Неверный токен'

    assert response_from_get_acsess_wrong.status_code == 400
    assert response_from_get_acsess_wrong_json["detail"] == expected_message














