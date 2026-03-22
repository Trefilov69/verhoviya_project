import pytest

@pytest.mark.django_db
def test_qr(client):
    response = client.post("/qr", {
        "batch_id": 1
    })
    assert response.status_code in [200, 201, 404]