BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
COURIER_URL = '/courier'
ORDERS_URL = '/orders'

class CourierData:
    VALID_COURIER_DATA = {
        "login": "the_flash",
        "password": "2014",
        "firstName": "TheFlash"
    }
    
    INVALID_COURIER_DATA = [
        {"password": "2014", "firstName": "TheFlash"},
        {"login": "the_flash", "firstName": "TheFlash"},
        {"firstName": "TheFlash"}
    ]

VALID_ORDER_DATA = {
    "firstName": "Barry",
    "lastName": "Allen",
    "address": "Central City, 56 apt.",
    "metroStation": 2,
    "phone": "+7 707 014 56 56",
    "rentTime": 5,
    "deliveryDate": "2026-06-26",
    "comment": "My Name Is Barry Allen I Am Fastest Man Alive",
    "color": []
}

class CourierErrorMessages:
    LOGIN_ALREADY_USED = "Этот логин уже используется. Попробуйте другой."
    INSUFFICIENT_DATA = "Недостаточно данных для создания учетной записи"
    COURIER_NOT_FOUND = "Курьера с таким id нет."
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    INSUFFICIENT_DATA_FOR_LOGIN = "Недостаточно данных для входа"

class OrderErrorMessages:
    pass  # Добавишь по мере необходимости

class SuccessMessages:
    OK_TRUE = '{"ok":true}'