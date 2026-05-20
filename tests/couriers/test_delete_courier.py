import allure
from methods.courier_methods import CourierMethods
import helpers


@allure.title('Тесты удаления курьера')
class TestDeleteCourier:
    
    @allure.title('Удалить курьера с валидными учетными данными - 200 (ok) + ok message')
    @allure.description('Сгенерировать данные, создать курьера, отправить запрос на удаление, проверить код ответа и сообщение')
    def test_delete_courier_valid_credentials_ok(self, courier_methods: CourierMethods, created_and_logged_courier):
        
        delete_response = courier_methods.delete_courier({"id": created_and_logged_courier["courier_id"]})

        assert delete_response.status_code == 200 and delete_response.text == '{"ok":true}'

    @allure.title('Удалить курьера без указания id - 404 (not found) + error message. Расходится с документацией')
    @allure.description('Отправить запрос на удаление с пустыми данными, проверить код ответа и сообщение')
    def test_delete_courier_empty_id_bad_request(self, courier_methods: CourierMethods):
        delete_params = {}
        error_message = 'Not Found.'

        delete_response = courier_methods.delete_courier(delete_params)

        assert delete_response.status_code == 404 and delete_response.json()['message'] == error_message

    @allure.title('Удалить курьера с неверным id - 404 (not found) + error message')
    @allure.description('Отправить запрос на удаление несуществующего курьера, проверить код ответа и сообщение')
    def test_delete_courier_wrong_id_bad_request(self, courier_methods: CourierMethods):
        delete_params = {'id': -1010101010}
        error_message = 'Курьера с таким id нет.'

        delete_response = courier_methods.delete_courier(delete_params)

        assert delete_response.status_code == 404 and delete_response.json()['message'] == error_message