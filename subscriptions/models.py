from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


User = get_user_model()


class Subscription(models.Model):
    NONE = 'none'
    BASIC = 'basic'
    FULL = 'full'


    SUBSCRIPTION_CHOICES = [
        (NONE, 'No Subscription'),
        (BASIC, 'Basic Subscription'),
        (FULL, 'Full Subscription'),
        ]
    
    PRICE_MAP = {
        NONE: 0,
        BASIC: 29,
        FULL: 59,
        }

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription', unique=True)
    plan = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default=NONE)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def discount_percentage(self):
        if self.plan == self.BASIC:
            return 30
        if self.plan == self.FULL:
            return 50
        return 0

    def price(self):
        return self.PRICE_MAP[self.plan]
    
    def activate(self, plan, duration_days=90):
        now = timezone.now()
        self.plan = plan

        if self.expires_at and self.expires_at > now:
            self.expires_at += timedelta(days=duration_days)
        else:
            self.started_at = now
            self.expires_at = now + timedelta(days=duration_days)

        self.save()

    def is_active(self):
        return self.expires_at and self.expires_at > timezone.now()

       
    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()}"

    def cleanup_duplicates(self):
        subs = Subscription.objects.filter(user=self.user).order_by('-expires_at')
        primary = subs.first()
        subs.exclude(id=primary.id).delete()
