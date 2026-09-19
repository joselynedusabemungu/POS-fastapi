import pytest


@pytest.mark.parametrize(
    "endpoint",
    [
        "/categories/",
        "/customers/",
        "/products/",
        "/payments/",
        "/receipts/",
        "/sales/",
        "/sale-items/",
        "/suppliers/",
        "/users/",
    ],
)
def test_entity_endpoints_require_authentication(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 401
