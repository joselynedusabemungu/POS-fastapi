def create_product(client, auth_headers):
    response = client.post(
        "/products/",
        json={"name": "Coca", "sku": "SALE-ITEM-1", "price": 5.50},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_sale(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    response = client.post(
        "/sales/",
        json={"total_amount": 11.00, "user_id": user_id},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_list_sale_items(client, auth_headers):
    response = client.get("/sale-items/", headers=auth_headers)
    assert response.status_code == 200


def test_create_sale_item(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 2, "unit_price": 5.50},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["quantity"] == 2
    assert response.json()["product_id"] == product_id


def test_get_sale_item(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 5.50},
        headers=auth_headers,
    )
    sale_item_id = response.json()["id"]
    response = client.get(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == sale_item_id


def test_update_sale_item(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 5.50},
        headers=auth_headers,
    )
    sale_item_id = response.json()["id"]
    response = client.put(
        f"/sale-items/{sale_item_id}",
        json={"quantity": 4},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 4


def test_delete_sale_item(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 5.50},
        headers=auth_headers,
    )
    sale_item_id = response.json()["id"]
    response = client.delete(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/sale-items/{sale_item_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_sale_item_with_missing_sale_returns_404(client, auth_headers):
    product_id = create_product(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": 99999, "product_id": product_id, "quantity": 1, "unit_price": 5.50},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_sale_item_with_missing_product_returns_404(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": 99999, "quantity": 1, "unit_price": 5.50},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_sale_item_with_missing_quantity_returns_422(client, auth_headers):
    product_id = create_product(client, auth_headers)
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "unit_price": 5.50},
        headers=auth_headers,
    )
    assert response.status_code == 422
