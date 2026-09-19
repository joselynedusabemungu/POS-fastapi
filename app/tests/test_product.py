def test_root(client):
    end_point = "/"  # arrange
    response = client.get(end_point)  # act
    assert response.status_code == 200  # assert


def test_list_products(client, auth_headers):
    end_point = "/products/"  # arrange
    response = client.get(end_point, headers=auth_headers)  # act
    assert response.status_code == 200  # assert


def test_create_product(client, auth_headers):
    product_data = {"name": "Coca", "sku": "SKU123", "price": 10.99}
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Coca"
    assert response.json()["sku"] == "SKU123"


def test_get_product(client, auth_headers):
    response = client.post(
        "/products/",
        json={"name": "Coca", "sku": "SKU124", "price": 10.99},
        headers=auth_headers,
    )
    product_id = response.json()["id"]
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == product_id


def test_update_product(client, auth_headers):
    product_data = {"name": "Coca", "sku": "SKU125", "price": 10.99}
    response = client.post("/products/", json=product_data, headers=auth_headers)
    product_id = response.json()["id"]
    updated_product = {"name": "Fanta", "sku": "SKU125", "price": 10.99}
    response = client.put(
        f"/products/{product_id}", json=updated_product, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Fanta"


def test_delete_product(client, auth_headers):
    product_data = {"name": "Coca", "sku": "SKU126", "price": 10.99}
    response = client.post("/products/", json=product_data, headers=auth_headers)
    product_id = response.json()["id"]
    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_product_with_missing_name_returns_422(client, auth_headers):
    product_data = {"sku": "SKU127", "price": 10.99}
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 422


def test_listing_products_without_credentials_returns_401(client):
    response = client.get("/products/")
    assert response.status_code == 401


def test_create_product_with_missing_category_returns_404(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "sku": "BAD-CATEGORY",
            "price": 10.99,
            "category_id": 99999,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_create_product_with_missing_supplier_returns_404(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "Invalid Product",
            "sku": "BAD-SUPPLIER",
            "price": 10.99,
            "supplier_id": 99999,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404
