import string
import copy
import requests
import allure
import random

from urls import  Endpoints
from data import  TestMessages


# класс содержит статические методы которые генерирует случайные валидные данные
class Generators:

    # метод генерирует случайную последовательность из строчных букв латинского алфавита
    @staticmethod
    @allure.step('Генерация случайной последовательности из строчных букв латинского алфавита')
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

        # метод генерирует случайную последовательность цифр в формате строки

    @staticmethod
    @allure.step('Генерация случайной последовательности цифр в формате строки')
    def generate_random_numbers_as_string(length):
        numbers = '0123456789'
        random_numbers = ''.join(random.choice(numbers) for _ in range(length))
        return random_numbers

    @staticmethod
    @allure.step('Генерация email')
    def generate_random_email():
        login_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3, 10)))
        email_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 6)))
        email_domain = ''.join(random.choices(string.ascii_lowercase, k=2))
        return f"{login_name}@{email_name}.{email_domain}"


    # статический метод генерирует список из валидных случайных: почты, пароля и имени
    @staticmethod
    @allure.step('Генерация пользователя')
    def generate_payload():
        email = (Generators.generate_random_email())
        password = Generators.generate_random_string(6) + Generators.generate_random_numbers_as_string(2)
        name = Generators.generate_random_string(5)
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return payload


# класс содержит статические методы для работы с пользователем
class User:

    # метод регистрирует нового пользователя
    @staticmethod
    @allure.step('Регистрация пользователя')
    def register_user(user):
        response = requests.post(url=Endpoints.CREATE_USER, json=user)
        return response

    # метод авторизует пользователя
    @staticmethod
    @allure.step('Авторизация пользователя')
    def login_user(authorization_user):
        registered_user_data_for_login = copy.deepcopy(authorization_user)
        del registered_user_data_for_login["name"]
        response = requests.post(url=Endpoints.LOGIN_USER, json=registered_user_data_for_login)
        return response

    # метод исключает заданную пару ключ-значение из регистрационных данных
    @staticmethod
    @allure.step('Исключить заданную пару ключ-значение')
    def excludes_parameter_from_user_registration_data(registered_user_data, exclude):
        data_copy = copy.deepcopy(registered_user_data)
        del data_copy[exclude]
        return data_copy

    # метод получает токен из запроса
    @staticmethod
    @allure.step('Получить токен авторизации')
    def get_access_token(response):
        allure.attach(str(response.json()), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)
        return response.json()["accessToken"]

    # метод изменяет значение регистрационных данных по ключу(исключает последний символ)
    @staticmethod
    @allure.step('Изменить тестовые данные')
    def change_parameter_value_in_user_registration_data(registered_user_data, change):
        data_copy = copy.deepcopy(registered_user_data)
        data_copy[change] = data_copy[change][:-1]
        return data_copy

    # метод удаляет пользователя после теста
    @staticmethod
    @allure.step('Удаление пользователя после теста')
    def delete_user_after_test(registered_user):
        with allure.step('Проверка перед удалением, что пользователь существует'):
            response = User.login_user(registered_user)
            if response.status_code == TestMessages.SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES["code"]:
                token = response.json()["accessToken"]
                header = {'Authorization': token}
                with allure.step('Запрос удаление пользователя'):
                    requests.delete(Endpoints.DELETE_USER, headers=header)
            else:
                with allure.step(f'Пользователь не существует или не авторизован, код ответа: {response.status_code}'):
                    allure.attach(str(response.json()), name="Ответ сервера", attachment_type=allure.attachment_type.JSON)





# класс содержит статистические методы для работы с заказом
class Order:

    # метод создаёт заказ
    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data, token=None):
        if token:
            header = {'Authorization': token}
            response = requests.post(url=Endpoints.CREATE_ORDER, headers=header, json=order_data)
        else:
            response = requests.post(url=Endpoints.CREATE_ORDER, json=order_data)
        return response


    # метод получает список ингредиентов
    @staticmethod
    @allure.step('Получить ингредиенты')
    def get_ingredients():
        response = requests.get(Endpoints.INGREDIENTS_INFO)
        return response.json()['data']


    # метод уменьшает код хеша на один последний символ
    @staticmethod
    @allure.step('Изменение хеша ингредиентов')
    def change_ingredients_hash(ingredients):
        return [item[:-1] for item in ingredients]


    # метод получает данные по заказу
    @staticmethod
    @allure.step('Получить данные по заказу пользователя')
    def get_users_order(token=None):
        if token:
            header = {'Authorization': token}
            response = requests.get(url=Endpoints.GET_ORDER_USER, headers=header)
        else:
            response = requests.get(url=Endpoints.GET_ORDER_USER)
        return response



