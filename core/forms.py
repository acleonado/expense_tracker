from django import forms
from .models import Account, Transaction
from django.forms.widgets import Select

from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name', 'balance')
        labels = {
            'name': 'Account Name',
            'balance': 'Starting Balance'
        }

TRANS_TYPE_CHOICES = (
    ('Income', 'Income'), 
    ('Expense', 'Expense'),
    ('Transfer', 'Transfer'),
)

class AddTransactionForm(forms.ModelForm):
    trans_type = forms.CharField(widget=forms.Select(choices=TRANS_TYPE_CHOICES), label='Transaction Type')
    date = forms.DateField(widget=DateInput())

    class Meta:
        model = Transaction
        fields = ('date', 'account', 'trans_type', 'desc', 'amount')
        labels = {
            'date': 'Date',
            'account': 'Account',
            'desc': 'Description',
            'amount': 'Amount'
        }