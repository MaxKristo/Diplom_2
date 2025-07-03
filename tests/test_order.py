import allure
from helpers import *
from urls import *


class TestCreateOrder:

    @allure.title('Проверка создания заказа без авторизации пользователя')
    @allure.description('Отправляем POST-запрос api/orders на создания заказа без авторизации пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_order_user_not_authorized(self, random_ingredients):
        payload = {"ingredients": random_ingredients}
        response = Order.create_order(payload)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()

    @allure.title('Проверка создания заказа авторизированного пользователя')
    @allure.description('Отправляем POST-запрос api/orders на создания заказа авторизированного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_order_authorized_user(self, register_user_with_random_data, random_ingredients):
        _, random_user = register_user_with_random_data
        login_response = User.login_user(random_user)
        token = User.get_access_token(login_response)
        payload = {"ingredients": random_ingredients}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        assert response.json()["success"] == TestMessages.ORDER_SUCCESSFUL_CREATION["success"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION["message"] in response.json()

    @allure.title('Проверка создания заказа без ингредиентов авторизированного пользователя')
    @allure.description('Отправляем POST-запрос api/orders на создания заказа без ингредиентов авторизированного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_order_without_ingredients_authorized_user(self, register_user_with_random_data):
        _, random_user = register_user_with_random_data
        login_response = User.login_user(random_user)
        token = User.get_access_token(login_response)
        payload = {"ingredients": {}}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["code"]
        assert response.json()["success"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["success"]
        assert response.json()["message"] == TestMessages.ORDER_NOT_CREATED_NO_INGREDIENTS["message"]

    @allure.title('Проверка создания заказа с неверным хешем ингредиентов авторизированного пользователя')
    @allure.description('Отправляем POST-запрос api/orders на создания заказа с неверным хешем авторизированного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_order_authorized_user_incorrect_hash(self, register_user_with_random_data, random_ingredients):
        _, random_user = register_user_with_random_data
        login_response = User.login_user(random_user)
        token = User.get_access_token(login_response)
        changed_ingredients = Order.change_ingredients_hash(random_ingredients)
        payload = {"ingredients": changed_ingredients}
        response = Order.create_order(payload, token=token)
        assert response.status_code == TestMessages.ORDER_NOT_CREATED_WRONG_HASH["code"]
        assert TestMessages.ORDER_NOT_CREATED_WRONG_HASH["text"] in response.text

