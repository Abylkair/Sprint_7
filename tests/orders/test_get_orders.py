import pytest
import allure
from methods.orders_methods import OrdersMethods

@allure.title('Тесты получения списка заказов')
class TestGetOrders:
    @allure.title('Получить разное количество заказов с 0 страницы - 200 (ok) + orders list len')
    @allure.description('Получить через параметризацию фильтры для списка заказов, отправить запрос на получение заказов, проверить код ответа и сообщение')
    @pytest.mark.parametrize("count", [1, 10, 30])
    def test_get_orders_variable_count_per_page_ok(self, count, orders_methods: OrdersMethods):
        params = {
            "limit": count
        }

        response = orders_methods.get_orders(params)

        assert response.status_code == 200 and len(response.json()['orders']) == count
    
    @allure.title('Получить заказы с разных страниц - 200 (ok) + orders list len > 0')
    @allure.description('Получить через параметризацию фильтры для списка заказов, отправить запрос на получение заказов, проверить код ответа и сообщение')
    @pytest.mark.parametrize("page", [0, 3, 10])
    def test_get_orders_variable_page_ok(self, page, orders_methods: OrdersMethods):
        params = {
            "page": page
        }

        response = orders_methods.get_orders(params)

        assert response.status_code == 200 and len(response.json()['orders']) > 0
    
    @allure.title('Получить заказы выбранного курьера - 200 (ok) + orders list len > 0')
    @allure.description('Через фикстуру создать и залогиниться курьером, добавить заказ в список, отправить запрос на получение заказов, проверить код ответа, сообщение и увеличенный список заказов')
    def test_get_orders_by_courier_id_ok_orders_count_increased(self, orders_methods: OrdersMethods, authorized_courier):
        courier_id = authorized_courier.json()['id']
        
        courier_orders_params = {
            "courierId": courier_id
        }
        # Получить список заказов курьера
        pre_orders = orders_methods.get_orders(courier_orders_params).json()['orders']

        get_orders_params = {
            "limit": 10
        }
        free_orders_response = orders_methods.get_orders(get_orders_params).json()['orders']
        free_order_id = free_orders_response[0]['id']

        accept_order_data = {
            "id": free_order_id,
            "courierId": courier_id
        }
        accept_response = orders_methods.accept_order(accept_order_data)
        
        post_orders = orders_methods.get_orders(courier_orders_params).json()['orders']

        assert accept_response.status_code == 200 and accept_response.text == '{"ok":true}' and len(post_orders) > len(pre_orders)