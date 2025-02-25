import requests

class TestHomeWorkCookie:
    def test_homework_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        cookies = response.cookies
        print(f"\nReceived cookies: {cookies}")

        assert "HomeWork" in cookies, "No 'HomeWork' cookie in response"

        expected_result = "hw_value"
        actual_result = cookies.get("HomeWork")
        print(f"Cookie 'HomeWork' value: {actual_result}")

        assert expected_result == actual_result, f"Unexpected cookie value: {actual_result}"
