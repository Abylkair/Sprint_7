import pytest
import allure
from methods.courier_methods import CourierMethods
import helpers
from data import CourierErrorMessages, SuccessMessages


@allure.title('Тесты создания курьера')
class TestCreateCourier:
    @allure.title('Создание курьера с уникальными данными - 201 (created) + ok message')
    @allure.description('Сгенерировать данные, отправить запрос на создание, проверить код ответа и сообщение')
    def test_create_courier_unique_data_created_ok_message(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()

        response = courier_methods.create_courier(params)

        assert response.status_code == 201 and response.text == SuccessMessages.OK_TRUE

    @allure.title('Создание курьера с неуникальными данными (попытка повторного создания) - 409 (conflict) + error message')
    @allure.description('Сгенерировать данные, отправить запрос на создание дважды, проверить код ответа и сообщение')
    def test_create_courier_nonunique_data_conflict_error_message(self, courier_methods: CourierMethods):
        params = helpers.generate_courier_data()

        response_unique = courier_methods.create_courier(params)
        response_nonunique = courier_methods.create_courier(params)

        assert (response_unique.status_code == 201 and 
                response_nonunique.status_code == 409 and 
                response_nonunique.json()['message'] == CourierErrorMessages.LOGIN_ALREADY_USED)

    @allure.title('Создание курьера с неполными учетными данными - 400 (bad request) + error message')
    @allure.description('Неполные данные для запросы берутся из параметризации, отправить запрос на создание, проверить код ответа и сообщение')
    @pytest.mark.parametrize("params", 
        [
            {"password": "pass123", "firstName": "First Name"},
            {"login": "log123", "firstName": "First Name"},
            {"firstName": "First Name"}
        ]
    )
    def test_create_courier_incomplete_data_bad_request_error_message(self, params, courier_methods: CourierMethods):
        response = courier_methods.create_courier(params)

        assert response.status_code == 400 and response.json()['message'] == CourierErrorMessages.INSUFFICIENT_DATA