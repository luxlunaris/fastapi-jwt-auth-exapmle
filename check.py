import json

from requests import get, post

response = post(
    "http://127.0.0.1:8001/sign-up",
    json.dumps(
        {
            "username": "test-user",
            "email": "test@assignit.com",
            "password": "test-password",
            "first_name": "Test",
            "last_name": "Testington",
        }
    ),
)

response = post(
    "http://127.0.0.1:8001/sign-in",
    json.dumps({"email": "test@assignit.com", "password": "test-password"}),
)
print(response.text)
authorization_cookies = response.cookies
print(authorization_cookies)
response = get("http://127.0.0.1:8001/sign-in")

response = post(
    "http://127.0.0.1:8001/sign-in",
    json.dumps({"email": "test@assignit.com", "password": "test-password"}),
    cookies=authorization_cookies,
)
print(response.json())
