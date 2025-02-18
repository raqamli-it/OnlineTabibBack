from django.contrib.auth import get_user_model
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="")  # Default qiymat berilgan

    def __str__(self):
        return self.name





User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('payme', 'Payme'),
        ('click', 'Click'),
        ('visa_mastercard', 'Visa/Mastercard'),
        ('uzcard_humo', 'Uzcard/Humo'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_method})"