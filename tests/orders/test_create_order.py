import pytest
import allure
from methods.orders_methods import OrdersMethods
from data import VALID_ORDER_DATA

@allure.title('Тесты создания заказов')
class TestCreateOrder:
    @allure.title('Создание заказа с разными цветами самокатов - 201 (created) + track id')
    @allure.description('Через параметризацию дополнить данные заказа, отправить запрос на создание заказа, проверить код ответа и присвоение номера заказа')
    @pytest.mark.parametrize("scooter_color", 
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            []
        ]
    )
    def test_create_order_black_grey_scooter_created(self, scooter_color, orders_methods: OrdersMethods):
        params = VALID_ORDER_DATA
        params["color"] = scooter_color

        response = orders_methods.create_order(params)

        assert response.status_code == 201 and response.json()['track']