from django.urls import path

from .views import LoanRequestList, LoanRequestDetail, LoanRequestStatusUpdate, loan_amortization_schedule

urlpatterns = [
    path("", LoanRequestList.as_view(), name="loan-request-list"),
    path("<int:pk>/", LoanRequestDetail.as_view(), name="loan-request-detail"),
    path("<int:pk>/status", LoanRequestStatusUpdate.as_view(), name="loan-request-status-update"),
    path("loan-amortized-schedule/", loan_amortization_schedule , name="loan-amortization-schedule"),
]