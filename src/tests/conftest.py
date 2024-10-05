from typing import Dict

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from loans.models import LoanRequest

User = get_user_model()

pytestmark = pytest.mark.django_db

@pytest.fixture
def client() -> APIClient:
    return APIClient()

@pytest.fixture
def test_user_data() -> Dict[str, object]:
    return {
        "email": "user1@test.com",
        "birth_date": "1999-04-02",
    }

@pytest.fixture
def test_other_user_data() -> Dict[str, object]:
    return {
        "email": "user2@test.com",
        "birth_date": "1999-04-02",
    }

@pytest.fixture
def test_user(test_user_data) -> User:
    obj =  User.objects.create(**test_user_data)
    return obj

@pytest.fixture
def test_other_user(test_other_user_data) -> User:
    obj =  User.objects.create(**test_other_user_data)
    return obj

@pytest.fixture
def test_admin_user() -> User:
    return User.objects.create(email="admin@test.com", is_superuser=True, is_staff=True)


@pytest.fixture
def auth_client(client, test_user) -> APIClient:
    user = User.objects.all().first()
    client.force_authenticate(user=user)

    return client

@pytest.fixture
def other_auth_client(client, test_other_user) -> APIClient:
    user = User.objects.all().first()
    client.force_authenticate(user=user)

    return client

@pytest.fixture
def auth_admin_client(client, test_admin_user) -> APIClient:
    user = User.objects.all().first()
    assert user.is_superuser
    assert user.is_staff
    client.force_authenticate(user=user)

    return client

@pytest.fixture
def test_loan_request(test_user) -> LoanRequest:
    obj: LoanRequest = LoanRequest.objects.create(amount=1000, term=30, user=test_user)
    assert LoanRequest.objects.all().count() == 1
    return obj