from django import forms
from .models import ConsultationPackage

class ConsultationPackageForm(forms.ModelForm):
    class Meta:
        model = ConsultationPackage
        fields = ['title', 'package_type', 'min_price', 'max_price', 'lawyer', 'description']