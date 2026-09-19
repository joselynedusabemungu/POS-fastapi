def create_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    response = client.post(
        "/sales/",
        json={"total_amount": 25.00, "user_id": user_id},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_list_payments(client, auth_headers):
    response = client.get("/payments/", headers=auth_headers)
    assert response.status_code == 200


def test_create_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "amount": 25.00, "payment_type": "Cash"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["sale_id"] == sale_id
    assert response.json()["payment_type"] == "Cash"


def test_get_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "amount": 25.00, "payment_type": "Card"},
        headers=auth_headers,
    )
    payment_id = response.json()["id"]
    response = client.get(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == payment_id


def test_update_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "amount": 25.00, "payment_type": "Cash"},
        headers=auth_headers,
    )
    payment_id = response.json()["id"]
    response = client.put(
        f"/payments/{payment_id}",
        json={"payment_type": "Card", "amount": 20.00},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["payment_type"] == "Card"
    assert response.json()["amount"] == "20.00"


def test_delete_payment(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "amount": 25.00, "payment_type": "Cash"},
        headers=auth_headers,
    )
    payment_id = response.json()["id"]
    response = client.delete(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_payment_with_missing_sale_returns_404(client, auth_headers):
    response = client.post(
        "/payments/",
        json={"sale_id": 99999, "amount": 10.00, "payment_type": "Cash"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_payment_with_missing_amount_returns_422(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "payment_type": "Cash"},
        headers=auth_headers,
    )
    assert response.status_code == 422
