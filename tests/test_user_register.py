import pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.feature("User Register API")
class TestUserRegister(BaseCase):

    @allure.title("Successfully create a user")
    @allure.description("This test checks the successful registration of a user via the API. "
                         "It ensures that the system allows the user to register and assigns them an ID.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("User Registration")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Create user with an existing email")
    @allure.description("This test checks that a user cannot be registered with an already existing email. "
                         "The system should respond with an error indicating the email is already in use.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("User Registration")
    @allure.tag("negative")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.title("Create user with an invalid email")
    @allure.description("This test checks what happens when an invalid email format is provided. "
                         "The system should respond with a 400 status and an appropriate error message.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.feature("User Registration")
    @allure.tag("negative")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("field", ["firstName", "lastName", "email", "password"])
    @allure.title("Create user without a required field")
    @allure.description("This test checks what happens when a required field is missing during user registration. "
                         "The system should return a 400 status and indicate which required field is missing.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.feature("User Registration")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_without_required_field(self, field):
        data = self.prepare_registration_data()
        data.pop(field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            f"Unexpected response content {response.content}"

    @allure.title("Create user with too short first name")
    @allure.description("This test checks what happens when the user's first name is too short. "
                         "The system should return an error indicating that the first name is too short.")
    @allure.severity(allure.severity_level.MINOR)
    @allure.feature("User Registration")
    @allure.tag("negative")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_with_too_short_first_name(self):
        short_name = 'A'
        data = self.prepare_registration_data(first_name=short_name)  # Name with 1 character

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.title("Create user with too long first name")
    @allure.description("This test checks what happens when the user's first name is too long. "
                         "The system should return an error indicating that the first name is too long.")
    @allure.severity(allure.severity_level.MINOR)
    @allure.feature("User Registration")
    @allure.tag("negative")
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_create_user_with_too_long_first_name(self):
        long_name = 'A' * 251
        data = self.prepare_registration_data(first_name=long_name)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", \
            f"Unexpected response content {response.content}"
