from rest_framework import serializers

from .models import LoanRequest

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['id', 'user', 'amount', 'term', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'user','created_at', 'updated_at']

class LoanRequestUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = ['status']