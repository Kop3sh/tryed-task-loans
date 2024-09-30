from django.urls import path

from .views import LoanRequestList, LoanRequestDetail

urlpatterns = [
    path("", LoanRequestList.as_view(), name="loanrequest-list"),
    path("<int:pk>/", LoanRequestDetail.as_view(), name="loanrequest-detail"),
]