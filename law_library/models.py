from django.db import models


class LawBook(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='law_books/', blank=True, null=True)
    alphabet = models.CharField(max_length=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Meta:
    ordering = ['title']


def save(self, *args, **kwargs):
    if self.title:
        self.alphabet = self.title[0].upper()
    super().save(*args, **kwargs)


def __str__(self):
    return f"{self.title} - {self.author}"
