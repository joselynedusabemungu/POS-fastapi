def create_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    response = client.post(
        "/sales/",
        json={"total_amount": 30.00, "user_id": user_id},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_list_receipts(client, auth_headers):
    response = client.get("/receipts/", headers=auth_headers)
    assert response.status_code == 200


def test_create_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "R-1001"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["receipt_number"] == "R-1001"


def test_get_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "R-1002"},
        headers=auth_headers,
    )
    receipt_id = response.json()["id"]
    response = client.get(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == receipt_id


def test_update_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "R-1003"},
        headers=auth_headers,
    )
    receipt_id = response.json()["id"]
    response = client.put(
        f"/receipts/{receipt_id}",
        json={"receipt_number": "R-1003-UPDATED"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["receipt_number"] == "R-1003-UPDATED"


def test_delete_receipt(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "R-1004"},
        headers=auth_headers,
    )
    receipt_id = response.json()["id"]
    response = client.delete(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/receipts/{receipt_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_receipt_with_missing_sale_returns_404(client, auth_headers):
    response = client.post(
        "/receipts/",
        json={"sale_id": 99999, "receipt_number": "BAD"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_receipt_with_missing_receipt_number_returns_422(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/", json={"sale_id": sale_id}, headers=auth_headers
    )
    assert response.status_code == 422
