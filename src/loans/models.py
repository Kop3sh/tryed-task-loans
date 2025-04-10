from django.db import models
from decimal import Decimal

REQUEST_STATUS = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

# NOTE: could go a generic way of using a ProductRequest model and create different Products (loans, credit cards, etc)


def validate_term(value):
    if value % Decimal(0.5) != 0:
        raise ValueError('Term of loan cannot be a fraction other than 0.5')

class LoanRequest(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_term])  # Allows values like 0.5, 2.0, 15.0, 30.0
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')

    user = models.ForeignKey('users.User', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # For finer grain control, we could use Django's permission system
    class Meta:
        permissions = [
            ("can_approve_loan", "Can approve loan request"),
            ("can_reject_loan", "Can reject loan request"),
        ]
