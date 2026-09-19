def test_register_user(client):
    user_data = {
        "username": "newuser",
        "password": "newpassword",
        "role": "Cashier",
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["role"] == "Cashier"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_register_duplicate_username_returns_400(client, test_user):
    response = client.post(
        "/auth/register",
        json={"username": test_user["username"], "password": "anotherpassword"},
    )
    assert response.status_code == 400


def test_login_returns_token(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_with_wrong_password_returns_401(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_auth_me_returns_current_user(client, auth_headers, test_user):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]


def test_protected_endpoint_without_credentials_returns_401(client):
    response = client.get("/categories/")
    assert response.status_code == 401
