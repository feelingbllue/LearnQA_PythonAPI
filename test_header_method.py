import requests

class TestHomeWorkHeader:
    def test_homework_header(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        headers = response.headers
        print(f"\nReceived headers: {headers}")

        assert "x-secret-homework-header" in headers, "No 'x-secret-homework-header' in response"

        expected_result = "Some secret value"
        actual_result = headers.get("x-secret-homework-header")
        print(f"Value of 'x-secret-homework-header': {actual_result}")

        assert expected_result == actual_result, "Unexpected header value: {actual_result}"