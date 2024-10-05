import pytest

from loans.models import LoanRequest

pytestmark = pytest.mark.django_db

loan_endpoint = "/loans/"


def test_unauth_user_cannot_create_loan_request(client):
    res = client.post(loan_endpoint, data={"amount": 1000, "term": 30})

    query = LoanRequest.objects.all()

    assert res.status_code == 401
    assert query.count() == 0

def test_any_auth_user_can_create_loan_request(auth_client):
    res = auth_client.post(loan_endpoint, data={"amount": 1000, "term": 30})

    query = LoanRequest.objects.all()

    assert res.status_code == 201

    assert query.count() == 1
    assert query.first().amount == 1000
    assert query.first().term == 30
    assert query.first().status == 'pending'
    assert query.first().user.pk == 1

def test_unauth_user_cannot_list_all_loan_requests(client, test_loan_request):
    res = client.get(loan_endpoint)

    assert res.status_code == 401

def test_auth_user_cannot_list_all_loan_requests(auth_client, test_loan_request):
    res = auth_client.get(loan_endpoint)

    assert res.status_code == 403

def test_auth_user_cannot_create_an_approved_loan(auth_client):
    res = auth_client.post(loan_endpoint, data={"amount": 1000, "term": 30, "status": "approved"})

    query = LoanRequest.objects.all()

    assert res.status_code == 201
    assert query.count() == 1
    assert query.first().status == 'pending'

def test_auth_user_cannot_create_loan_for_other_usres(auth_client, test_other_user):
    res = auth_client.post(loan_endpoint, data={"amount": 1000, "term": 30, "user": test_other_user.pk})

    query = LoanRequest.objects.all()

    assert res.status_code == 201
    assert query.count() == 1
    assert query.first().user.pk == 1
    assert test_other_user.pk != 1