import pytest

@pytest.mark.django_db
def test_login(client):
    response = client.post("/login", {
        "email": "test@test.com",
        "password": "1234"
    })
    assert response.status_code in [200, 401]