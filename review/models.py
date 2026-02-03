from django.db import models
from django.conf import settings


class LawyerReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(
        'search_lawyer.Lawyer', on_delete=models.CASCADE,
        related_name='reviews')
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lawyer')

    def __str__(self):
        return f"{self.lawyer.name} - {self.rating}★"


class PackageReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(
        'consultation_packages.ConsultationPackage',
        on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'package')

    def __str__(self):
        return f"{self.package.title} - {self.rating}★"
