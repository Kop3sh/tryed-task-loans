from decimal import Decimal
import pytest

from loans.models import LoanRequest

pytestmark = pytest.mark.django_db

loan_endpoint = "/loans/"

def test_unauth_user_cannot_get_loan_request_detail(client, test_loan_request):
    res = client.get(loan_endpoint + "1/")

    assert LoanRequest.objects.all().count() == 1
    assert res.status_code == 401

def test_auth_user_can_get_his_own_loan_request_detail(auth_client, test_loan_request):
    res = auth_client.get(loan_endpoint + "1/")

    assert LoanRequest.objects.all().count() == 1
    assert res.status_code == 200
    assert Decimal(res.data["amount"]) == test_loan_request.amount
    assert Decimal(res.data["term"]) == test_loan_request.term

def test_auth_user_cannot_get_other_users_loan_request_detail(other_auth_client, test_loan_request):
    res = other_auth_client.get(loan_endpoint + "1/")

    assert LoanRequest.objects.all().count() == 1
    assert res.status_code == 403

def test_admin_user_can_get_other_users_loan_request_detail(auth_admin_client, test_loan_request):
    res = auth_admin_client.get(loan_endpoint + "1/")

    assert LoanRequest.objects.all().count() == 1
    assert res.status_code == 200
    assert Decimal(res.data["amount"]) == test_loan_request.amount
    assert Decimal(res.data["term"]) == test_loan_request.term