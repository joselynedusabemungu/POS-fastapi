def test_list_categories(client, auth_headers):
    response = client.get("/categories/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_create_category(client, auth_headers):
    category_data = {"name": "Soft Drinks", "description": "Cold drinks"}
    response = client.post("/categories/", json=category_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Soft Drinks"


def test_get_category(client, auth_headers):
    response = client.post(
        "/categories/", json={"name": "Snacks"}, headers=auth_headers
    )
    category_id = response.json()["id"]
    response = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == category_id


def test_update_category(client, auth_headers):
    response = client.post(
        "/categories/", json={"name": "Old Name"}, headers=auth_headers
    )
    category_id = response.json()["id"]
    response = client.put(
        f"/categories/{category_id}",
        json={"name": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_category(client, auth_headers):
    response = client.post(
        "/categories/", json={"name": "Temporary"}, headers=auth_headers
    )
    category_id = response.json()["id"]
    response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_category_with_missing_name_returns_422(client, auth_headers):
    response = client.post("/categories/", json={}, headers=auth_headers)
    assert response.status_code == 422
