from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Lawyer(models.Model):
    SOLICITOR = 'solicitor'
    ADVOCATE = 'advocate'

    LAWYER_TYPE_CHOICES = [
        (SOLICITOR, 'Solicitor'),
        (ADVOCATE, 'Advocate'),
        ]

    CONTRACTS = 'contracts'
    DEEDS = 'deeds'
    FAMILY = 'family'
    COMMERCIAL = 'commercial'
    CRIMINAL = 'criminal'


# For solicitors: specialities
    SPECIALITY_CHOICES = [
        ('contracts', 'Contracts'),
        ('deeds', 'Deeds'),
        ('family', 'Family'),
        ('commercial', 'Commercial'),
        ('criminal', 'Criminal'),
        ]


# For advocates: court levels
    COURT_LEVEL_CHOICES = [
        ('magistrate', "Magistrate's Court"),
        ('high', 'High Court'),
        ('appeal', 'Appeal Court'),
        ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='lawyer_profile',
        null=True, blank=True)
    name = models.CharField(max_length=255)
    lawyer_type = models.CharField(
        max_length=20, choices=LAWYER_TYPE_CHOICES, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    # other fields
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # solicitor-specific
    specialty = models.CharField(
        max_length=50, choices=SPECIALITY_CHOICES, blank=True, null=True)

    # advocate-specific
    court_level = models.CharField(
        max_length=50, choices=COURT_LEVEL_CHOICES, blank=True, null=True)

    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='media/lawyers/', blank=True, null=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']


def __str__(self):
    return f"{self.name} ({self.get_lawyer_type_display()})"
