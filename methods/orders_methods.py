import requests
import allure

class OrdersMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url

    @allure.step('Запрос создания заказа (POST + JSON-data)')
    def create_order(self, data):
        response = requests.post(
            url=self.namespace_url,
            json=data
        )
        return response
    
    @allure.step('Запрос получения заказов (GET + params)')
    def get_orders(self, params):
        response = requests.get(
            url=self.namespace_url,
            params=params
        )
        return response

    @allure.step('Запрос добавления заказа курьеру (PUT + params)')
    def accept_order(self, data):
        id = data['id']
        params = {"courierId": data['courierId']}
        response = requests.put(
            url=f'{self.namespace_url}/accept/{id}',
            params=params
        )
        return response