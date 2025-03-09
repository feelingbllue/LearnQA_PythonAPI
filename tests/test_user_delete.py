import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature("User Deletion API")
class TestUserDelete(BaseCase):

    @allure.title("Test: Try to delete special user (ID 2)")
    @allure.description("This test checks if the system prevents deleting special users with ID 1, 2, 3, 4, and 5. "
                         "User with ID 2 should not be deletable.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_delete_special_user(self):
        login_data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        response3 = MyRequests.get("/user/2")

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', \
            f"Unexpected response content: {response2.content}"
        Assertions.assert_code_status(response3, 200)
        assert response3.content.decode("utf-8") == '{"username":"Vitaliy"}', \
            f"Unexpected response content: {response3.content}"

    @allure.title("Test: Successfully delete user")
    @allure.description("This test checks the scenario where a user successfully deletes their own account. "
                         "After deletion, the user should not be found when trying to access their details.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_delete_user_successfully(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")

        login_data = {'email': register_data['email'], 'password': register_data['password']}
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", \
            f"Unexpected response content: {response4.content}"

    @allure.title("Test: Try to delete another user's account")
    @allure.description("This test checks the scenario where a user tries to delete another user's account. "
                         "The system should prevent a user from deleting accounts of other users.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://playground.learnqa.ru/api/map", name="API Documentation")
    def test_delete_user_as_another_user(self):
        login_data = {'email': 'test09@test.test', 'password': '1111'}
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        another_user_id = user_id_from_auth - 1
        response2 = MyRequests.delete(
            f"/user/{another_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"This user can only delete their own account."}', \
            f"Unexpected response content: {response2.content}"
