import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)

redirects_count = len(response.history)
final_url = response.url

print(f"Number of redirects: {redirects_count}")
print(f"Final URL: {final_url}")
