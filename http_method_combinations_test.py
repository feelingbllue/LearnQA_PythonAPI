import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

print(f"{'~'*50}")

response = requests.get(url)
print(f"Response without method parameter: {response.text}")

response = requests.head(url)
print(f"Response for HEAD request: {response.text}")

response = requests.put(url, params={"method": "PUT"})
print(f"Response with correct method 'PUT': {response.text}")


methods = ["GET", "POST", "PUT", "DELETE"]
request_types = ["GET", "POST", "PUT", "DELETE"]

for request_type in request_types:
    for method in methods:
        print(f"{'~'*30}")
        print(f"Request: {request_type} with method {method}")
        if request_type == "GET":
            response = requests.get(url,params={"method": method})
        elif request_type == "POST":
            response = requests.post(url,data={"method": method})
        elif request_type == "PUT":
            response = requests.put(url,data={"method": method})
        elif request_type == "DELETE":
            response = requests.delete(url,data={"method": method})

        print(f"Response: {response.text}")
