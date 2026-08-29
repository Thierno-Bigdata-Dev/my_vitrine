from django import forms
from .models import PlanPayment

class PlanPaymentForm(forms.ModelForm):
    class Meta:
        model = PlanPayment
        fields = ['payment_method', 'phone_number', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 77 123 45 67'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saisissez l\'ID de transaction reçu par SMS'}),
        }
