# payments/models.py
from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('square', 'Square'),
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

