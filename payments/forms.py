from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)


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
