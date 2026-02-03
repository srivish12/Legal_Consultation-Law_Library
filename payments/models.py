from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from subscriptions.models import Subscription
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
    CONSULTATION_PACKAGE = 'consultation_package'
    SUBSCRIPTION = 'subscription'

    PAYMENT_TYPE_CHOICES = [
        (CONSULTATION_PACKAGE, 'Consultation_Package'),
        (SUBSCRIPTION, 'Subscription'),
    ]

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        null=True, blank=True

    )

    subscription_plan = models.CharField(
        max_length=10,
        null=True, blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    package = models.ForeignKey(
        'consultation_packages.ConsultationPackage',
        on_delete=models.CASCADE, null=True, blank=True
    )

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

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

        subscription = Subscription.objects.filter(
            user=self.user,
            expires_at__gt=timezone.now()
        ).first()

        if subscription:
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
