import json

import bs4


def test_auth(client, clean_test_data) -> None:
    """Authentication scenarios check"""
    response = client.post("/sign-out")
    assert response.json()["detail"] == "Missing cookie access_token_cookie"
    assert response.status_code == 401

    response = client.post(
        "/sign-up",
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
    assert response.json()["message"] == "User has been created"
    assert response.status_code == 201

    response = client.post(
        "/sign-up",
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
    assert response.json()["message"] == "User with such email already exists"
    assert response.status_code == 400

    response = client.post(
        "/sign-in",
        json.dumps({"email": "test@assignit.com", "password": "wrong-test-password"}),
    )
    assert response.json()["message"] == "Invalid email or password"
    assert response.status_code == 401

    response = client.post(
        "/sign-in",
        json.dumps({"email": "test@assignit.com", "password": "test-password"}),
    )
    assert response.json()["message"] == "Authorized successfully"
    assert "access_token_cookie" in response.cookies
    assert response.status_code == 200

    authorization_cookies = response.cookies
    headers = {"X-CSRF-Token": authorization_cookies["csrf_access_token"]}
    del authorization_cookies["csrf_access_token"]

    response = client.post(
        "/sign-in",
        json.dumps({"email": "test@assignit.com", "password": "test-password"}),
        cookies=authorization_cookies,
        headers=headers,
    )
    assert response.json()["message"] == "You have signed in already"
    assert response.status_code == 400

    response = client.post(
        "/sign-up",
        json.dumps(
            {
                "username": "test-user-repeat",
                "email": "test-repeat@assignit.com",
                "password": "test-password",
                "first_name": "Test",
                "last_name": "Testington",
            }
        ),
        cookies=authorization_cookies,
        headers=headers,
    )
    assert response.json()["message"] == "Cannot create new user when signed in"
    assert response.status_code == 400

    response = client.post("/sign-out", cookies=authorization_cookies, headers=headers)
    assert response.status_code == 200
    assert "access_cookie_token" not in response.cookies
    assert "csrf_access_token" not in response.cookies
