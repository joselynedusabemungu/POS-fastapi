def test_root(client):
    end_point = "/"  #arrange
    response = client.get(end_point)  #act
    assert response.status_code == 200  #assert
