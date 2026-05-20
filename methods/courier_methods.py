import requests
import allure

class CourierMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url

    @allure.step('Запрос создания курьера (POST + JSON-data)')
    def create_courier(self, data):
        response = requests.post(
            url=self.namespace_url,
            json=data
        )
        return response

    @allure.step('Запрос удаления курьера (DELETE + JSON-data)')
    def delete_courier(self, data):
        id = data.get('id', '')
        response = requests.delete(
            url=f'{self.namespace_url}/{id}',
            json=data
        )
        return response
    
    @allure.step('Запрос логина курьера (POST + JSON-data + timeout=10)')
    def login_courier(self, data):
        response = requests.post(
            url=f'{self.namespace_url}/login',
            json=data,
            timeout=10
        )
        return response