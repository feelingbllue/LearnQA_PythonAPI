import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Create a new job
response = requests.get(url)
response_json = response.json()

seconds = response_json['seconds']
token = response_json['token']

print(f"Task created.\n Waiting time: {seconds} seconds.\n Token: {token}\n")

# BEFORE waiting
response_before = requests.get(url, params={"token": token})
response_before_json = response_before.json()

print(f"Status before waiting: {response_before_json['status']}")

# Wait for the specified time
print(f"Waiting for {seconds} seconds...\n")
time.sleep(seconds)

# AFTER waiting
response_after = requests.get(url, params={"token": token})
response_after_json = response_after.json()

if response_after_json['status'] == "Job is ready":
    print(f"Job is really ready! Result: {response_after_json['result']}")
else:
    print(f"Job is NOT ready: {response_after_json['status']}")
