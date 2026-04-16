from django import forms
from .models import Lawyer

class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = [
            'name',
            'specialty',
            'experience_years',
            'court_level',
            'bio',
            'hourly_rate',
            'profile_picture',
            'is_available',
            'lawyer_type',
            'phone',
            'email',
        ]

    def clean_experience_years(self):
        years = self.cleaned_data.get('experience_years')
        if years < 0:
            raise forms.ValidationError("Experience cannot be negative.")
        return years
