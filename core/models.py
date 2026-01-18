from django.db import models


class SiteSettings(models.Model):
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Site Social Media Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
# Create your models here.
