import pytest
import helpers
from methods.courier_methods import CourierMethods
from methods.orders_methods import OrdersMethods
from data import BASE_URL, COURIER_URL, ORDERS_URL


@pytest.fixture
def orders_methods() -> OrdersMethods:
    orders_namespace_url = f'{BASE_URL}{ORDERS_URL}'
    orders_methods = OrdersMethods(orders_namespace_url)
    return orders_methods


@pytest.fixture
def courier_methods() -> CourierMethods:
    courier_namespace_url = f'{BASE_URL}{COURIER_URL}'
    courier_methods = CourierMethods(courier_namespace_url)
    return courier_methods


@pytest.fixture
def authorized_courier(courier_methods: CourierMethods):
    create_params = helpers.generate_courier_data()
    create_response = courier_methods.create_courier(create_params)
    if create_response.status_code == 201:
        login_params = {
            "login": create_params['login'],
            "password": create_params['password']
        }
        login_response = courier_methods.login_courier(login_params)
        yield login_response
    else:
        raise Exception('Что-то пошло не так, проверьте параметры запроса')
    delete_params = {'id': login_response.json()['id']}
    courier_methods.delete_courier(delete_params)


@pytest.fixture
def created_and_logged_courier(courier_methods: CourierMethods):
    create_params = helpers.generate_courier_data()
    create_response = courier_methods.create_courier(create_params)
    
    # 1. Сначала подготавливаем параметры и логинимся
    login_params = {
        "login": create_params['login'],
        "password": create_params['password']
    }
    login_response = courier_methods.login_courier(login_params)
    
    if login_response.status_code != 200:
        pytest.fail(f"Не удалось залогиниться в фикстуре. Статус: {login_response.status_code}")
    
    courier_data = {
        "courier_id": login_response.json()['id'],
        "login": create_params['login'],
        "password": create_params['password'],
        "create_params": create_params
    }
    
    yield courier_data
    
    delete_params = {"id": courier_data["courier_id"]}
    courier_methods.delete_courier(delete_params)