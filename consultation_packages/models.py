from django.db import models
from search_lawyer.models import Lawyer



class ConsultationPackage(models.Model):
    DOCUMENT_HANDLING = 'document'
    CONSULTATION_ONLY = 'consultation'
    COURT_APPEARANCE = 'court'


    PACKAGE_TYPE_CHOICES = [
        (DOCUMENT_HANDLING, 'Document handling'),
        (CONSULTATION_ONLY, 'Consultation only'),
        (COURT_APPEARANCE, 'Court appearance'),
    ]


    title = models.CharField(max_length=255)
    package_type = models.CharField(max_length=30, choices=PACKAGE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, null=True, blank=True, related_name='packages')


    def __str__(self):
        lawyer_name = self.lawyer.name if self.lawyer else "No Lawyer"
        return f"{self.title} - {lawyer_name} - {self.get_package_type_display()}"