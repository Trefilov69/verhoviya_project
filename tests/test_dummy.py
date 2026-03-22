import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@test.com",
        password="123456"
    )
    assert user.email == "test@test.com"


@pytest.mark.django_db
def test_user_password():
    user = User.objects.create_user(
        email="test2@test.com",
        password="123456"
    )
    assert user.check_password("123456") is True


@pytest.mark.django_db
def test_user_not_empty():
    User.objects.create_user(
        email="test3@test.com",
        password="123456"
    )
    assert User.objects.count() == 1


def test_math():
    assert 2 + 2 == 4


def test_string():
    assert "abc".upper() == "ABC"