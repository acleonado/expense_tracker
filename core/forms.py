from django import forms
from .models import Account, Transaction
from django.forms.widgets import Select

from functools import partial
from django.urls import reverse
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        labels = {
            'name': 'Account Name',
            'balance': 'Starting Balance'
        }
        
class AddTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput())

    class Meta:
        model = Transaction
        fields = ['date', 'account', 'trans_type', 'desc', 'amount']
        labels = {
            'date': 'Date',
            'account': 'Account',
            'trans_type': 'Transaction Type',
            'desc': 'Description',
            'amount': 'Amount'
        }