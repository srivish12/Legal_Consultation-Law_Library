from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)

    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    expiry_month = forms.IntegerField(min_value=1, max_value=12)
    expiry_year = forms.IntegerField(min_value=2024, max_value=2035)
    cvv = forms.CharField(max_length=4, min_length=3)
    cardholder_name = forms.CharField(max_length=100)

    widgets = {
    'full_name': forms.TextInput(attrs={'class': 'form-control'}),
    'email': forms.EmailInput(attrs={'class': 'form-control'}),
    'phone': forms.TextInput(attrs={'class': 'form-control'}),
    'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
    'cardholder_name': forms.TextInput(attrs={'class': 'form-control'}),
    'card_number': forms.TextInput(attrs={'class': 'form-control'}),
    'expiry_month': forms.Select(attrs={'class': 'form-control'}),
    'expiry_year': forms.Select(attrs={'class': 'form-control'}),
    'cvv': forms.PasswordInput(attrs={'class': 'form-control'}),
    }
