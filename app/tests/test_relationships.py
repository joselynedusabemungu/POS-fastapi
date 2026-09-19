def create_category(client, auth_headers):
    response = client.post(
        "/categories/", json={"name": "Beverages"}, headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"company_name": "Supplier Co", "contact_info": "contact"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_product(client, auth_headers, category_id=None, supplier_id=None, sku="REL-1"):
    payload = {"name": "Product", "sku": sku, "price": 10.00}
    if category_id is not None:
        payload["category_id"] = category_id
    if supplier_id is not None:
        payload["supplier_id"] = supplier_id
    response = client.post("/products/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    return response.json()["id"]


def create_customer(client, auth_headers):
    response = client.post(
        "/customers/",
        json={"first_name": "John", "last_name": "Customer", "email": "rel@example.com"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_sale(client, auth_headers, customer_id=None):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    payload = {"total_amount": 20.00, "user_id": user_id}
    if customer_id is not None:
        payload["customer_id"] = customer_id
    response = client.post("/sales/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    return response.json()["id"]


def create_sale_item(client, auth_headers, sale_id, product_id):
    response = client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 1, "unit_price": 10.00},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_category_can_be_deleted_while_product_references_it(client, auth_headers):
    category_id = create_category(client, auth_headers)
    product_id = create_product(client, auth_headers, category_id=category_id, sku="REL-CAT")
    response = client.delete(f"/categories/{category_id}", headers=auth_headers)
    assert response.status_code == 204
    product = client.get(f"/products/{product_id}", headers=auth_headers)
    assert product.status_code == 200
    assert product.json()["category_id"] is None


def test_supplier_can_be_deleted_while_product_references_it(client, auth_headers):
    supplier_id = create_supplier(client, auth_headers)
    product_id = create_product(client, auth_headers, supplier_id=supplier_id, sku="REL-SUP")
    response = client.delete(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == 204
    product = client.get(f"/products/{product_id}", headers=auth_headers)
    assert product.status_code == 200
    assert product.json()["supplier_id"] is None


def test_product_cannot_be_deleted_while_sale_item_references_it(client, auth_headers):
    product_id = create_product(client, auth_headers, sku="REL-PROD")
    sale_id = create_sale(client, auth_headers)
    create_sale_item(client, auth_headers, sale_id, product_id)
    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 409


def test_customer_can_be_deleted_while_sale_references_it(client, auth_headers):
    customer_id = create_customer(client, auth_headers)
    sale_id = create_sale(client, auth_headers, customer_id=customer_id)
    response = client.delete(f"/customers/{customer_id}", headers=auth_headers)
    assert response.status_code == 204
    sale = client.get(f"/sales/{sale_id}", headers=auth_headers)
    assert sale.status_code == 200
    assert sale.json()["customer_id"] is None


def test_user_cannot_be_deleted_while_sale_references_it(client, auth_headers):
    user_id = client.get("/users/", headers=auth_headers).json()[0]["id"]
    create_sale(client, auth_headers)
    response = client.delete(f"/users/{user_id}", headers=auth_headers)
    assert response.status_code == 409


def test_sale_cannot_be_deleted_while_sale_item_references_it(client, auth_headers):
    product_id = create_product(client, auth_headers, sku="REL-SALE-ITEM")
    sale_id = create_sale(client, auth_headers)
    create_sale_item(client, auth_headers, sale_id, product_id)
    response = client.delete(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == 409


def test_sale_cannot_be_deleted_while_payment_references_it(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/payments/",
        json={"sale_id": sale_id, "amount": 20.00, "payment_type": "Cash"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    response = client.delete(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == 409


def test_sale_cannot_be_deleted_while_receipt_references_it(client, auth_headers):
    sale_id = create_sale(client, auth_headers)
    response = client.post(
        "/receipts/",
        json={"sale_id": sale_id, "receipt_number": "REL-RECEIPT"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    response = client.delete(f"/sales/{sale_id}", headers=auth_headers)
    assert response.status_code == 409
