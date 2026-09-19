def test_duplicate_product_sku_returns_409(client, auth_headers):
    payload = {"name": "Coca", "sku": "UNIQUE-1", "price": 10.00}
    first = client.post("/products/", json=payload, headers=auth_headers)
    assert first.status_code == 201
    second = client.post("/products/", json=payload, headers=auth_headers)
    assert second.status_code == 409


def test_duplicate_customer_email_returns_409(client, auth_headers):
    payload = {
        "first_name": "Joselyne",
        "last_name": "Dusabemungu",
        "email": "unique@example.com",
    }
    first = client.post("/customers/", json=payload, headers=auth_headers)
    assert first.status_code == 201
    second = client.post("/customers/", json=payload, headers=auth_headers)
    assert second.status_code == 409


def test_duplicate_receipt_number_returns_409(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    sale_one = client.post(
        "/sales/",
        json={"total_amount": 10.00, "user_id": user_id},
        headers=auth_headers,
    ).json()["id"]
    sale_two = client.post(
        "/sales/",
        json={"total_amount": 20.00, "user_id": user_id},
        headers=auth_headers,
    ).json()["id"]

    first = client.post(
        "/receipts/",
        json={"sale_id": sale_one, "receipt_number": "UNIQUE-RECEIPT"},
        headers=auth_headers,
    )
    assert first.status_code == 201

    second = client.post(
        "/receipts/",
        json={"sale_id": sale_two, "receipt_number": "UNIQUE-RECEIPT"},
        headers=auth_headers,
    )
    assert second.status_code == 409


def test_duplicate_receipt_for_same_sale_returns_409(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    sale_id = client.post(
        "/sales/",
        json={"total_amount": 10.00, "user_id": user_id},
        headers=auth_headers,
    ).json()["id"]

    first = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "RECEIPT-1"},
        headers=auth_headers,
    )
    assert first.status_code == 201

    second = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "RECEIPT-2"},
        headers=auth_headers,
    )
    assert second.status_code == 409
