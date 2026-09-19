def test_list_customers(client, auth_headers):
    response = client.get("/customers/", headers=auth_headers)
    assert response.status_code == 200


def test_create_customer(client, auth_headers):
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
    }
    response = client.post("/customers/", json=customer_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["first_name"] == "John"


def test_get_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={"first_name": "Jane", "last_name": "Doe"},
        headers=auth_headers,
    )
    customer_id = response.json()["id"]
    response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == customer_id


def test_update_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={"first_name": "Jane", "last_name": "Doe"},
        headers=auth_headers,
    )
    customer_id = response.json()["id"]
    response = client.put(
        f"/customers/{customer_id}",
        json={"first_name": "Janet"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Janet"


def test_delete_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={"first_name": "Temporary", "last_name": "Customer"},
        headers=auth_headers,
    )
    customer_id = response.json()["id"]
    response = client.delete(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_customer_with_missing_first_name_returns_422(client, auth_headers):
    response = client.post(
        "/customers/", json={"last_name": "Doe"}, headers=auth_headers
    )
    assert response.status_code == 422
