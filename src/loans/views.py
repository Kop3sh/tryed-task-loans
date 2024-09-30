
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics

from .models import LoanRequest
from .serializers import LoanRequestSerializer
from treyd.permissions import OwnsOrIsAdmin



class LoanRequestList(generics.ListCreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer


class LoanRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer
    permission_classes = [OwnsOrIsAdmin]
