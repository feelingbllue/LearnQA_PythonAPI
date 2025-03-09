import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.feature("User Edit API")
class TestUserEdit(BaseCase):

    @allure.title("Test: Successfully edit user details after registration")
    @allure.description("This test checks the process of user registration, login, and updating user details "
                         "such as first name through the API. It ensures that user data can be edited successfully.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_user_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.title("Test: Edit user details without authentication")
    @allure.description("This test checks if a user can edit another user's details without being authenticated. "
                         "It ensures that the system denies unauthorized requests for user data editing.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_edit_user_not_auth(self):
        new_name = "New Name"

        response = MyRequests.put(
            "/user/10",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == '{"error":"Auth token not supplied"}', \
            f"Unexpected response content: {response.content}"

    @allure.title("Test: Edit another user's details")
    @allure.description("This test checks if a user can edit another user's details. "
                         "It ensures that the system denies access to modify data of another user.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_edit_user_as_another_user(self):
        login_data = {'email': 'test09@test.test', 'password': '1111'}
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        another_user_id = user_id_from_auth - 1
        another_name = "Changed Name"
        response2 = MyRequests.put(
            f"/user/{another_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": another_name}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"This user can only edit their own data."}', \
            f"Unexpected response content: {response2.content}"

    @allure.title("Test: Edit user with invalid email format")
    @allure.description("This test checks the response when a user tries to edit their email with an invalid format. "
                         "It ensures that the system rejects invalid email formats during the edit process.")
    @allure.severity(allure.severity_level.MINOR)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_edit_user_invalid_email(self):
        login_data = {'email': 'test08@test.test', 'password': '1111'}
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        new_email = "invalid_email.com"
        response2 = MyRequests.put(
            f"/user/{user_id_from_auth}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"Invalid email format"}', \
            f"Unexpected response content: {response2.content}"

    @allure.title("Test: Edit user with too short first name")
    @allure.description("This test checks the response when a user tries to edit their first name with too few characters. "
                         "It ensures that the system rejects first names that are too short.")
    @allure.severity(allure.severity_level.MINOR)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_edit_user_too_short_firstname(self):
        login_data = {'email': 'test03@test.test', 'password': '1111'}
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        new_first_name = "A"
        response2 = MyRequests.put(
            f"/user/{user_id_from_auth}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_first_name}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"The value for field `firstName` is too short"}', \
            f"Unexpected response content: {response2.content}"
