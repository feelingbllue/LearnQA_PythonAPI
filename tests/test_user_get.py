import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.feature("User Get API")
class TestUserGet(BaseCase):

    @allure.title("Test: Get user details without authentication")
    @allure.description("This test checks if user details can be accessed without authentication. "
                         "It ensures that only the username is returned and other personal data is not exposed.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Test: Get user details with same user authentication")
    @allure.description("This test checks if a user can access their own details after authenticating with valid credentials. "
                         "It ensures that the user sees all personal information like username, email, first name, and last name.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_get_user_details_auth_with_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234',
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Test: Get user details with different user authentication")
    @allure.description("This test checks if a user can access another user's details when authenticated. "
                         "It ensures that the system does not return sensitive information from other users.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_get_user_details_auth_with_different_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234',
        }

        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        different_user_id = user_id_from_auth_method + 1
        response2 = MyRequests.get(
            f"/user/{different_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")
