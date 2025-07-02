import random
import pytest
import allure
from helpers import Generators, User, Order




# фикстура регистрирует нового пользователя и удаляет его после теста
@pytest.fixture()
def register_user_with_random_data():
    with allure.step('Создание случайных регистрационных данных пользователя'):
        random_user = Generators.generate_payload()
        response = User.register_user(random_user)
        if response.status_code == 200:
            yield response, random_user
            User.delete_user_after_test(random_user)
        else:
            pytest.fail(f"Пользователь не зарегистрирован: {response.status_code}, {response.text}")


# фикстура генерирует случайные данные пользователя, передаёт их в тест и удаляет пользователя после теста
@pytest.fixture()
def random_user_data():
    with allure.step('Создание случайных регистрационных данных пользователя'):
        random_user = Generators.generate_payload()
        yield random_user
        User.delete_user_after_test(random_user)


# фикстура генерирует случайный список из трёх ингредиентов
@pytest.fixture()
def random_ingredients():
    with allure.step('Создание случайного списка из трёх ингредиентов'):
        ingredients = Order.get_ingredients()
        random_ingredient_1 = random.choice(ingredients)
        random_ingredient_2 = random.choice(ingredients)
        random_ingredient_3 = random.choice(ingredients)
        yield [random_ingredient_1["_id"],
                random_ingredient_2["_id"],
                random_ingredient_3["_id"]
        ]