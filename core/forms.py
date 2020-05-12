from django import forms
from .models import Account, Budget, AccountTransaction, BudgetTransaction
from django.forms.widgets import Select
from functools import partial
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
    input_type = 'date'


TRANS_TYPE_CHOICES = (
    ('Income', 'Income'), 
    ('Expense', 'Expense'),
)

TRANSF_TYPE_CHOICES = (
    ('Transfer', 'Transfer'), 
)

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'balance']
        labels = {
            'name': 'Account Name',
            'balance': 'Starting Balance'
        }

    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)
        self.fields['balance'].widget.attrs['min'] = 1
        self.fields['name'].widget.attrs['class'] = 'account-name'
        self.fields['balance'].widget.attrs['class'] = 'account-balance'

class AddBudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['account', 'name']
        labels = {
            'name': 'Budget Name',
            'account': 'Account Name'
        }

    def __init__(self, current_user, *args, **kwargs):
        super(AddBudgetForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(username=current_user)
        self.fields['account'].widget.attrs['class'] = 'budget-account'
        self.fields['name'].widget.attrs['class'] = 'budget-name'

class AddAccountTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    trans_type = forms.ChoiceField(choices = TRANS_TYPE_CHOICES, label = 'Transaction Type')

    class Meta:
        model = AccountTransaction
        fields = ['date', 'account', 'trans_type', 'desc', 'amount']
        labels = {
            'date': 'Date',
            'account': 'Account',
            'desc': 'Description',
            'amount': 'Amount'
        }

    def __init__(self, current_user, *args, **kwargs):
        super(AddAccountTransactionForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(username=current_user)
        self.fields['amount'].widget.attrs['min'] = 1
        # self.fields['amount'].widget.attrs['class'] = 'form-control'

class MakeTransferForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    trans_type = forms.ChoiceField(choices = TRANSF_TYPE_CHOICES, label = 'Transaction Type')

    class Meta:
        model = AccountTransaction
        fields = ['date', 'account', 'budget','trans_type', 'desc', 'amount']
        labels = {
            'date': 'Date',
            'account': 'From (Account)',
            'budget': 'To (Budget)',
            'desc': 'Description',
            'amount': 'Amount'
        }

    def __init__(self, current_user, *args, **kwargs):
        super(MakeTransferForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(username=current_user)
        self.fields['budget'].queryset = Budget.objects.filter(account__username=current_user)
        self.fields['amount'].widget.attrs['min'] = 1
        self.fields['trans_type'].widget.attrs['readonly'] = True

class AddBudgetTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = BudgetTransaction
        fields = ['date', 'budget', 'trans_type', 'desc', 'amount']
        labels = {
            'date': 'Date',
            'budget': 'Budget Name',
            'trans_type': 'Transaction Type',
            'desc': 'Description',
            'amount': 'Amount'
        }
    
    def __init__(self, current_user, *args, **kwargs):
        super(AddBudgetTransactionForm, self).__init__(*args, **kwargs)
        self.fields['budget'].queryset = Budget.objects.filter(account__username=current_user)
        self.fields['trans_type'].widget.attrs['readonly'] = True
        self.fields['amount'].widget.attrs['min'] = 1