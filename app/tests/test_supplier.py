def test_list_suppliers(client, auth_headers):
    response = client.get("/suppliers/", headers=auth_headers)
    assert response.status_code == 200


def test_create_supplier(client, auth_headers):
    supplier_data = {"company_name": "ABC Supplies", "contact_info": "123456789"}
    response = client.post("/suppliers/", json=supplier_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["company_name"] == "ABC Supplies"


def test_get_supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"company_name": "ABC", "contact_info": "abc@example.com"},
        headers=auth_headers,
    )
    supplier_id = response.json()["id"]
    response = client.get(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == supplier_id


def test_update_supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"company_name": "Old Supplier", "contact_info": "old"},
        headers=auth_headers,
    )
    supplier_id = response.json()["id"]
    response = client.put(
        f"/suppliers/{supplier_id}",
        json={"company_name": "New Supplier"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["company_name"] == "New Supplier"


def test_delete_supplier(client, auth_headers):
    response = client.post(
        "/suppliers/",
        json={"company_name": "Temporary", "contact_info": "temp"},
        headers=auth_headers,
    )
    supplier_id = response.json()["id"]
    response = client.delete(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/suppliers/{supplier_id}", headers=auth_headers)
    assert response.status_code == 404


def test_create_supplier_with_missing_contact_info_returns_422(client, auth_headers):
    response = client.post(
        "/suppliers/", json={"company_name": "ABC"}, headers=auth_headers
    )
    assert response.status_code == 422
