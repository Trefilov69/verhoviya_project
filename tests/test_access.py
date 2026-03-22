import pytest


@pytest.mark.django_db
def test_access_unauthorized(client):
    """
    Проверяем, что без авторизации доступ к batch закрыт
    """
    response = client.get("/batches/9999/")
    assert response.status_code in (403, 404)


@pytest.mark.django_db
def test_access_homepage(client):
    """
    Простой тест — проверяем, что сервер отвечает
    """
    response = client.get("/")
    assert response.status_code in (200, 301, 302, 404)