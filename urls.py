URL = 'https://stellarburgers.nomoreparties.site/'

class Endpoints:

# Request_URL
    LOGIN_USER = f"{URL}api/auth/login"          # для авторизации пользователя
    CREATE_USER = f"{URL}api/auth/register"      # для регистрации пользователя
    DELETE_USER = f"{URL}api/auth/user"          # для удаления пользователя
    CHANGE_USER_DATA = f"{URL}api/auth/user"     # для изменений данных пользователя

    INGREDIENTS_INFO = f"{URL}api/ingredients"   # для получения данных об ингредиентах
    CREATE_ORDER = f"{URL}api/orders"             # для создания заказа
    GET_ORDER_USER = f"{URL}api/orders"          # для получения заказа конкретного пользователя

