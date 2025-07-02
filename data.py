# класс содержит КОДЫ и СООБЩЕНИЕ ответов на запросы
class TestMessages:

    # создание пользователя
    SUCCESSFUL_CREATED_NEW_USER_WITH_VALID_VALUES = {"code": 200, "success": True, "message": "accessToken"}
    USER_LOGIN_ALREADY_IN_USE = {"code": 403, "success": False, "message": "User already exists"}
    USER_NOT_CREATED_WITHOUT_REGISTER_DATA = {"code": 403, "success": False, "message": "Email, password and name are required fields"}
    USER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES = {"code": 200, "success": True, "message": "accessToken"}
    AUTHORIZATION_DATA_NOT_ENOUGH = {"code": 401, "success": False, "message": "email or password are incorrect"}
    USER_DELETE = {"code": 202, "success": True, "message": "User successfully removed"}
    USER_SUCCESSFUL_UPDATE_DATA = {"code": 200, "success": True, "message": "user"}
    NOT_SUCCESSFUL_CHANGE_DATA_OF_NOT_AUTHORIZED_USER = {"code": 401, "success": False, "message": "You should be authorised"}
    NOT_SUCCESSFUL_CHANGE_DATA_DUPLICATE_EMAIL = {"code": 403, "success": False, "message": "User with such email already exists"}

    # создание заказа
    ORDER_SUCCESSFUL_CREATION = {"code": 200, "success": True, "message": "order"}
    ORDER_NOT_CREATED_WRONG_HASH = {"code": 500, "text": "Internal Server Error"}
    ORDER_NOT_CREATED_NO_INGREDIENTS = {"code": 400, "success": False, "message": "Ingredient ids must be provided"}
    GET_ORDER_NOT_AUTHORIZED_USER = {"code": 401, "success": False, "message": "You should be authorised"}
    GET_ORDER_AUTHORIZED_USER = {"code": 200, "success": True, "message": "orders"}

class RequiredParameters:

# переменная, которая содержит параметры используемые при регистрации пользователя
    register_parameters = ["email", "password", "name"]

# переменная, которая содержит параметры используемые при авторизации пользователя
    login_parameters = ["email", "password"]