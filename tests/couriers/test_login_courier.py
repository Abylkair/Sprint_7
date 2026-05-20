import pytest
import allure
from methods.courier_methods import CourierMethods
import helpers

@allure.title('Тесты логина курьера')
class TestLoginCourier:

    @allure.title('Залогиниться под валидными учетными данными - 200 (ok) + id')
    @allure.description(
        'Создать курьера с валидными данными, '
        'отправить запрос на логин, проверить код ответа и id'
    )
    def test_login_courier_valid_credentials_ok(
        self,
        courier_methods: CourierMethods
    ):
        courier_data = helpers.generate_courier_data()

        courier_methods.create_courier(courier_data)

        params = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }

        response = courier_methods.login_courier(params)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body.get("id") is not None

    @allure.title(
        'Залогиниться без указания логина или пароля - '
        '400 (bad request) + error message'
    )
    @allure.description(
        'Создать курьера, отправить запрос на логин '
        'с неполными данными, проверить ошибку'
    )
    @pytest.mark.parametrize(
        "params",
        [
            {"password": "test_password"}
        ]
    )
    def test_login_courier_incomplete_credentials_bad_request(
        self,
        params,
        courier_methods: CourierMethods
    ):
        courier_data = helpers.generate_courier_data()
        courier_methods.create_courier(courier_data)

        error_message = 'Недостаточно данных для входа'

        response = courier_methods.login_courier(params)
        response_body = response.json()

        assert response.status_code == 400
        assert response_body.get("message") == error_message

    @allure.title(
        'Залогиниться под несуществующими учетными данными - '
        '404 (not found) + error message'
    )
    @allure.description(
        'Сгенерировать уникальные логин-пароль, '
        'отправить запрос без создания курьера'
    )
    def test_login_courier_invalid_credentials_not_found(
        self,
        courier_methods: CourierMethods
    ):
        params = helpers.generate_courier_data()

        login_params = {
            "login": params["login"],
            "password": params["password"]
        }

        error_message = 'Учетная запись не найдена'

        response = courier_methods.login_courier(login_params)
        response_body = response.json()

        assert response.status_code == 404
        assert response_body.get("message") == error_message

    @allure.title(
        'Залогиниться с неверным паролем '
        'для существующего курьера - '
        '404 (not found) + error message'
    )
    @allure.description(
        'Создать курьера, отправить запрос '
        'с неверным паролем'
    )
    def test_login_courier_wrong_password_not_found(
        self,
        courier_methods: CourierMethods
    ):
        courier_data = helpers.generate_courier_data()

        courier_methods.create_courier(courier_data)

        params = {
            "login": courier_data["login"],
            "password": f"{courier_data['password']}_wrong"
        }

        error_message = 'Учетная запись не найдена'

        response = courier_methods.login_courier(params)
        response_body = response.json()

        assert response.status_code == 404
        assert response_body.get("message") == error_message