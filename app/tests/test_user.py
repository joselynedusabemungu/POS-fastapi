def test_list_users(client, auth_headers, test_user):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()[0]["username"] == test_user["username"]


def test_create_user(client, auth_headers):
    user_data = {"username": "newuser", "password": "newpassword", "role": "Admin"}
    response = client.post("/users/", json=user_data, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["role"] == "Admin"
    assert "password" not in response.json()


def test_get_user(client, auth_headers, second_user):
    user_id = second_user["id"]
    response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user(client, auth_headers, second_user):
    user_id = second_user["id"]
    response = client.put(
        f"/users/{user_id}",
        json={"username": "renameduser", "role": "Admin"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["username"] == "renameduser"
    assert response.json()["role"] == "Admin"


def test_update_user_password(client, auth_headers, second_user):
    user_id = second_user["id"]
    response = client.put(
        f"/users/{user_id}",
        json={"password": "changedpassword"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    response = client.post(
        "/auth/login",
        data={"username": "seconduser", "password": "changedpassword"},
    )
    assert response.status_code == 200


def test_delete_user(client, auth_headers, second_user):
    user_id = second_user["id"]
    response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_duplicate_username_returns_400(client, auth_headers, test_user):
    response = client.post(
        "/users/",
        json={"username": test_user["username"], "password": "another"},
        headers=auth_headers,
    )
    assert response.status_code == 400
