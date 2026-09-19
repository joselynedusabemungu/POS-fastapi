def create_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={"first_name": "John", "last_name": "Doe", "email": "sale@example.com"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_sale(client, auth_headers, user_id, customer_id=None):
    payload = {"total_amount": 25.50, "user_id": user_id}
    if customer_id is not None:
        payload["customer_id"] = customer_id
    response = client.post("/sales/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    return response.json()


def test_list_sales(client, auth_headers):
    response = client.get("/sales/", headers=auth_headers)
    assert response.status_code == 200


def test_create_sale(client, auth_headers, test_user):
    response = client.get("/users/", headers=auth_headers)
    user_id = response.json()[0]["id"]
    sale = create_sale(client, auth_headers, user_id)
    assert sale["total_amount"] == "25.50"
    assert sale["user_id"] == user_id


def test_get_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    sale = create_sale(client, auth_headers, user_id)
    response = client.get(f"/sales/{sale['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == sale["id"]


def test_update_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    customer_id = create_customer(client, auth_headers)
    sale = create_sale(client, auth_headers, user_id, customer_id)
    response = client.put(
        f"/sales/{sale['id']}",
        json={"total_amount": 50.00},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["total_amount"] == "50.00"


def test_delete_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    sale = create_sale(client, auth_headers, user_id)
    response = client.delete(f"/sales/{sale['id']}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/sales/{sale['id']}", headers=auth_headers)
    assert response.status_code == 404


def test_create_sale_with_missing_user_returns_404(client, auth_headers):
    response = client.post(
        "/sales/",
        json={"total_amount": 10.00, "user_id": 99999},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_sale_with_missing_customer_returns_404(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    response = client.post(
        "/sales/",
        json={"total_amount": 10.00, "user_id": user_id, "customer_id": 99999},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_sale_with_missing_total_amount_returns_422(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    response = client.post(
        "/sales/", json={"user_id": user_id}, headers=auth_headers
    )
    assert response.status_code == 422
