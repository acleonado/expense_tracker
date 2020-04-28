from django import forms
from .models import Account

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'balance')
        labels = {
            'name': 'Account Name',
            'balance': 'Starting Balance'
        }