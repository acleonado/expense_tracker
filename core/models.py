from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

TRANS_TYPE_CHOICES = (
    ('Income', 'Income'), 
    ('Expense', 'Expense'),
)

class Account(models.Model):
    name = models.CharField(max_length = 25)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Budget(models.Model):
    name = models.CharField(max_length = 25)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class AccountTransaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    trans_type = models.CharField(max_length = 15, choices=TRANS_TYPE_CHOICES)
    desc = models.CharField(max_length = 50)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return str(self.date) + ' | ' + str(self.account) + ' | ' + str(self.amount)

class BudgetTransaction(models.Model):
    date = models.DateField()
    budget = models.ForeignKey(Budget, on_delete = models.CASCADE)
    trans_type = models.CharField(max_length = 15, choices=TRANS_TYPE_CHOICES)
    desc = models.CharField(max_length = 50)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return str(self.date) + ' | ' + str(self.account) + ' | ' + str(self.amount)