import pytest
from helpers import *
from urls import *
import copy
import allure
from data import *



class TestCreateUser:

    @allure.title('Проверка успешного создания пользователя с валидными данными')
    @allure.description('Отправляем POST-запрос на ручку api/auth/register на создание пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_user_with_valid_values(self, register_user_with_random_data):
        response, _ = register_user_with_random_data
        assert response.status_code == TestMessages.SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES["code"]
        assert response.json()["success"] == TestMessages.SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES["success"]
        assert TestMessages.SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES["message"] in response.json()


    @allure.title('Проверка, что нельзя создать двух одинаковых пользователей')
    @allure.description('Отправляем POST-запрос на ручку api/auth/register на невозможность создание пользователя дважды и и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_create_user_login_already_in_use(self, register_user_with_random_data):
        _, random_user = register_user_with_random_data
        response = User.register_user(random_user)
        assert response.status_code == TestMessages.USER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["success"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["success"]
        assert response.json()["message"] == TestMessages.USER_LOGIN_ALREADY_IN_USE["message"]

    @allure.title('Проверка регистрации пользователя - json не содержит обязательного поля')
    @allure.description('Отправляем POST-запрос на ручку api/auth/register на создание пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    # параметризация для полей, которые обязательны
    @pytest.mark.parametrize("field_to_exclude", RequiredParameters.register_parameters)
    def test_create_user_without_required_field(self, random_user_data, field_to_exclude):
        payload = User.excludes_parameter_from_user_registration_data(random_user_data, exclude=field_to_exclude)
        response = User.register_user(payload)
        assert response.status_code == TestMessages.USER_NOT_CREATED_WITHOUT_REGISTER_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_NOT_CREATED_WITHOUT_REGISTER_DATA["success"]
        assert response.json()["message"] == TestMessages.USER_NOT_CREATED_WITHOUT_REGISTER_DATA["message"]


class TestAuthorizationUser:

    @allure.title('Проверка авторизации существующего пользователя с валидными данными')
    @allure.description('Отправляем POST-запрос на ручку api/auth/login на авторизацию созданного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_authorization_user_with_valid_values(self, register_user_with_random_data):
        _, random_user = register_user_with_random_data
        response = User.login_user(random_user)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES["success"]
        assert TestMessages.USER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES["message"] in response.json()


    @allure.title('Проверка невозможности авторизации существующего пользователя с указанием неверных данных обязательного поля')
    @allure.description('Отправляем POST-запрос на ручку api/auth/login на авторизацию пользователя с указанием неверного обязательного поля и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    @pytest.mark.parametrize("change_param", RequiredParameters.login_parameters)
    def test_not_authorization_user_with_wrong_credentials(self, register_user_with_random_data, change_param):
        _, random_user = register_user_with_random_data
        payload = User.change_parameter_value_in_user_registration_data(random_user, change_param)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["code"]
        assert response.json()["success"] == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["success"]
        assert response.json()["message"] == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["message"]


    @allure.title('Проверка авторизации существующего пользователя - json не содержит обязательного поля- "login" или "password"')
    @allure.description('Отправляем POST-запрос на ручку POST-запрос на ручку api/auth/login на авторизацию пользователя без указания обязательного поля и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    @pytest.mark.parametrize("exclude_param", RequiredParameters.login_parameters)
    def test_authorization_user_without_required_fields(self, register_user_with_random_data, exclude_param):
        _, random_user = register_user_with_random_data
        payload = User.excludes_parameter_from_user_registration_data(random_user, exclude=exclude_param)
        response = User.login_user(payload)
        assert response.status_code == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["code"]
        assert response.json()["success"] == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["success"]
        assert response.json()["message"] == TestMessages.AUTHORIZATION_DATA_NOT_ENOUGH["message"]


class TestEditUser:

    @allure.title('Проверка возможности изменить поле параметра, авторизованного пользователя')
    @allure.description('Отправляем запрос PATCH-запрос на ручку api/auth/user на изменение значения параметра авторизованного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    @pytest.mark.parametrize("change_param", RequiredParameters.register_parameters)
    def test_change_data_of_authorized_user(self, register_user_with_random_data, change_param):
        _, random_user = register_user_with_random_data
        random_user_data_for_login = copy.deepcopy(random_user)
        login_response = User.login_user(random_user_data_for_login)
        token = User.get_access_token(login_response)
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user,change=change_param)
        random_user.update(updated_user_data)
        response = User.edit_user(random_user, token)
        assert response.status_code == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["code"]
        assert response.json()["success"] == TestMessages.USER_SUCCESSFUL_UPDATE_DATA["success"]
        assert TestMessages.USER_SUCCESSFUL_UPDATE_DATA["message"] in response.json()

    @allure.title('Проверка возможности изменить поле параметра, НЕ авторизованного пользователя')
    @allure.description('Отправляем запрос PATCH-запрос на ручку api/auth/user на изменение значения параметра НЕ авторизованного пользователя и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    @pytest.mark.parametrize("change_param", RequiredParameters.register_parameters)
    def test_change_data_not_authorized_user(self, register_user_with_random_data, change_param):
        _, random_user = register_user_with_random_data
        updated_user_data = User.change_parameter_value_in_user_registration_data(random_user,change=change_param)
        response = User.edit_user(updated_user_data)
        assert response.status_code == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_OF_NOT_AUTHORIZED_USER["code"]
        assert response.json()["success"] == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_OF_NOT_AUTHORIZED_USER["success"]
        assert response.json()["message"] == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_OF_NOT_AUTHORIZED_USER["message"]

    @allure.title('Проверка возможности передать email, которая уже используется для существующего пользователя')
    @allure.description('Отправляем запрос PATCH-запрос на ручку api/auth/user на изменение email существующего пользователя, который уже используется и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Stellar Burgers»')
    def test_edit_user_data_authorized_user_duplicate_email(self, register_user_with_random_data, random_user_data):
        _, random_user = register_user_with_random_data
        User.register_user(random_user_data)
        random_user_data_for_login = copy.deepcopy(random_user)
        login_response = User.login_user(random_user_data_for_login)
        token = User.get_access_token(login_response)
        data_for_update = {
            "email": random_user_data["email"],
            "password": random_user["password"],
            "name": random_user["name"]
        }
        response = User.edit_user(data_for_update, token)
        assert response.status_code == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_DUPLICATE_EMAIL["code"]
        assert response.json()["success"] == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_DUPLICATE_EMAIL["success"]
        assert response.json()["message"] == TestMessages.NOT_SUCCESSFUL_CHANGE_DATA_DUPLICATE_EMAIL["message"]