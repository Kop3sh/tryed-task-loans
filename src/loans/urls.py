from django.urls import path

from .views import LoanRequestList, LoanRequestDetail, LoanRequestStatusUpdate
# from .views import create_loan_request

urlpatterns = [
    path("", LoanRequestList.as_view(), name="loan-request-list"),
    path("<int:pk>/", LoanRequestDetail.as_view(), name="loan-request-detail"),
    path("<int:pk>/status", LoanRequestStatusUpdate.as_view(), name="loan-request-status-update"),
]