# класс содержит КОДЫ и СООБЩЕНИЕ ответов на запросы
class TestMessages:

    # создание пользователя
    SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES = {"code": 200, "success": True, "message": "accessToken"}
    USER_LOGIN_ALREADY_IN_USE = {"code": 403, "success": False, "message": "User already exists"}
    USER_NOT_CREATED_WITHOUT_REGISTER_DATA = {"code": 403, "success": False, "message": "Email, password and name are required fields"}
    USER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES = {"code": 200, "success": True, "message": "accessToken"}
    AUTHORIZATION_DATA_NOT_ENOUGH = {"code": 401, "success": False, "message": "email or password are incorrect"}
    USER_DELETE = {"code": 202, "success": True, "message": "User successfully removed"}

    # создание заказа
    ORDER_SUCCESSFUL_CREATION = {"code": 200, "success": True, "message": "order"}
    ORDER_NOT_CREATED_WRONG_HASH = {"code": 500, "text": "Internal Server Error"}
    ORDER_NOT_CREATED_NO_INGREDIENTS = {"code": 400, "success": False, "message": "Ingredient ids must be provided"}

class RequiredParameters:

# переменная, которая содержит параметры используемые при регистрации пользователя
    register_parameters = ["email", "password", "name"]

# переменная, которая содержит параметры используемые при авторизации пользователя
    login_parameters = ["email", "password"]


