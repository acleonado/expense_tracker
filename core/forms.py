from django import forms
from .models import Account, Budget, AccountTransaction
from django.forms.widgets import Select
from functools import partial
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        labels = {
            'name': 'Account Name',
            'balance': 'Starting Balance'
        }

class AddBudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['account', 'name', 'balance']
        labels = {
            'name': 'Budget Name',
            'account': 'Account Name',
            'balance': 'Starting Balance'
        }

    def __init__(self, current_user, *args, **kwargs):
        super(AddBudgetForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(username=current_user)
 

class AddAccountTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput())

    class Meta:
        model = AccountTransaction
        fields = ['date', 'account', 'trans_type', 'desc', 'amount']
        labels = {
            'date': 'Date',
            'account': 'Account',
            'trans_type': 'Transaction Type',
            'desc': 'Description',
            'amount': 'Amount'
        }

    def __init__(self, current_user, *args, **kwargs):
        super(AddAccountTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(username=current_user)