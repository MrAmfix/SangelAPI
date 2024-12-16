from time import sleep
from src.tests.testlib import api_requests
from src.settings import VERIFICATION_CODE_EXPIRE_SECONDS
from datetime import datetime, timedelta
from src.tests.conftest import run_async, change_create_time, create_visibility_type


def test_send_sms():

    payload = "+71234567890"

    response = api_requests.send_sms_api_request(phone=payload)
    response_json = response.json()
    expected_message = "Код отправлен"

    assert response.status_code == 200
    assert response_json["detail"] == expected_message

    time_expire_value = datetime.now() - timedelta(
        seconds=int(VERIFICATION_CODE_EXPIRE_SECONDS) + 300
    )
    run_async(change_create_time, payload, time_expire_value)

    wrong_payload = "+71234567"
    response = api_requests.send_sms_api_request(phone=wrong_payload)
    response_json = response.json()

    expected_message = "Неправильно указан номер телефона"

    assert response.status_code == 400
    assert response_json["detail"] == expected_message

    time_expire_value_less_than_expire = datetime.now() + timedelta(
        seconds=int(VERIFICATION_CODE_EXPIRE_SECONDS) - 20
    )

    run_async(change_create_time, payload, time_expire_value_less_than_expire)

    response = api_requests.send_sms_api_request(phone=payload)
    response_json = response.json()

    expected_message = f"Код уже был отправлен ранее, повторная отправка возможна раз в {VERIFICATION_CODE_EXPIRE_SECONDS} секунд"

    assert response.status_code == 429
    assert response_json["detail"] == expected_message


def test_check_sms():

    payload = "+71234567890"
    response = api_requests.send_sms_api_request(phone=payload)

    payload = {"phone": "+71234567890", "code": "111111"}
    response = api_requests.get_code_api_request(payload=payload)
    response_json = response.json()

    expected_message = "Код верен"

    assert response.status_code == 200
    assert response_json["detail"] == expected_message

    payload = {"phone": "+71234567890", "code": "111112"}
    response = api_requests.get_code_api_request(payload=payload)
    response_json = response.json()

    expected_message = "Неправильный код"

    assert response.status_code == 400
    assert response_json["detail"] == expected_message

    payload = {"phone": "+71234567", "code": "111111"}
    response = api_requests.get_code_api_request(payload=payload)
    response_json = response.json()

    expected_message = "Неверно указан номер телефона"

    assert response.status_code == 400
    assert response_json["detail"] == expected_message


def test_registration(create_test_user):

    run_async(create_visibility_type)

    response = api_requests.registration_api_request(user=create_test_user)
    assert response.status_code == 200


def test_get_access(create_test_user):

    run_async(create_visibility_type)

    response_from_registration = api_requests.registration_api_request(
        user=create_test_user
    )

    assert response_from_registration.status_code == 200

    response_json = response_from_registration.json()
    refresh_token = response_json.get("refresh_token")

    sleep(1)    # Поставил задержку, потому что не успевало записывать токен в бд и при получении токена вылетает ошибка

    response_from_get_access = api_requests.get_access_api_request(token=refresh_token)

    assert response_from_get_access.status_code == 200

    wrong_refresh_token = "wrong_token_value"

    response_from_get_access_wrong = api_requests.get_access_api_request(
        token=wrong_refresh_token
    )
    response_from_get_access_wrong_json = response_from_get_access_wrong.json()
    expected_message = "Неверный токен"

    assert response_from_get_access_wrong.status_code == 400
    assert response_from_get_access_wrong_json["detail"] == expected_message
