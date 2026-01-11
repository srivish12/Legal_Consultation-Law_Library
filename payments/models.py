from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from consultation_packages.models import ConsultationPackage

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]

    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    package = models.ForeignKey(
        'consultation_packages.ConsultationPackage',
        on_delete=models.CASCADE, null=True, blank=True
    )

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    original_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_percent = models.PositiveIntegerField(default=0)

    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    
    
    def apply_subscription_discount(self):
        """
        Apply discount based on user's active subscription.
        """
        percent = 0

        subscription = getattr(self.user, 'subscription', None)
        if subscription and subscription.is_active():
            percent = subscription.discount_percent()

        discount = (self.original_amount * Decimal(percent)) / Decimal(100)
        self.discount_percent = percent
        self.final_amount = self.original_amount - discount
        self.save(update_fields=[
            'discount_percent',
            'final_amount'
        ])

    def mark_completed(self):
        self.status = self.COMPLETED
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])

    def __str__(self):
        return f"Payment #{self.id} - {self.user} - {self.status}"

