from django import forms
from .models import LawyerReview, PackageReview


class LawyerReviewForm(forms.ModelForm):
    class Meta:
        model = LawyerReview
        fields = ['rating', 'comment']


class PackageReviewForm(forms.ModelForm):
    class Meta:
        model = PackageReview
        fields = ['rating', 'comment']
