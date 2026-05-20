import pytest
import allure
from methods.courier_methods import CourierMethods
import helpers
from data import CourierData, CourierErrorMessages, SuccessMessages


@allure.title('Тесты создания курьера')
class TestCreateCourier:
    @allure.title('Создание курьера с уникальными данными - 201 (created) + ok message')
    def test_create_courier_unique_data_created_ok_message(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()
        
        response = courier_methods.create_courier(params)
        
        assert response.status_code == 201
        assert response.text == SuccessMessages.OK_TRUE
        
        login_response = courier_methods.login_courier({
            "login": params['login'],
            "password": params['password']
        })
        courier_methods.delete_courier({"id": login_response.json()['id']})

    @allure.title('Создание курьера с неуникальными данными - 409')
    def test_create_courier_nonunique_data_conflict_error_message(self, courier_methods: CourierMethods):
        params = CourierData.VALID_COURIER_DATA.copy()
        
        courier_methods.create_courier(params)
        response = courier_methods.create_courier(params)
        
        assert response.status_code == 409
        assert response.json()['message'] == CourierErrorMessages.LOGIN_ALREADY_USED
        
        # удаление
        login_response = courier_methods.login_courier({
            "login": params['login'],
            "password": params['password']
        })
        courier_methods.delete_courier({"id": login_response.json()['id']})

    @allure.title('Создание курьера с неполными данными - 400')
    @pytest.mark.parametrize("params", CourierData.INVALID_COURIER_DATA)
    def test_create_courier_incomplete_data_bad_request_error_message(self, params, courier_methods: CourierMethods):
        response = courier_methods.create_courier(params)

        assert response.status_code == 400 and response.json()['message'] == CourierErrorMessages.INSUFFICIENT_DATA