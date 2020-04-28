from django.db import models
from djmoney.models.fields import MoneyField

class Account(models.Model):
    name = models.CharField(max_length = 25)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    def __str__(self):
        return str(self.name)

# class Transaction(models.Model):
#     date = models.DateField()
#     account = models.ForeignKey(Account, )