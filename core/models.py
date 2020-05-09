from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length = 25)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Budget(models.Model):
    name = models.CharField(max_length = 25)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default = '0.00')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class AccountTransaction(models.Model):
    date = models.DateField()
    account = models.ForeignKey(Account, on_delete = models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete = models.CASCADE, null=True)
    trans_type = models.CharField(max_length = 15)
    desc = models.CharField(max_length = 50)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return str(self.date) + ' | ' + str(self.account) + ' | ' + str(self.amount)

class BudgetTransaction(models.Model):
    date = models.DateField()
    budget = models.ForeignKey(Budget, on_delete = models.CASCADE, related_name= 'budgettransaction')
    trans_type = models.CharField(max_length = 15, default="Expense")
    desc = models.CharField(max_length = 50)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return str(self.date) + ' | ' + str(self.budget) + ' | ' + str(self.amount)