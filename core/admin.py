from django.contrib import admin
from .models import Account, Budget, AccountTransaction, BudgetTransaction

admin.site.register(Account)
admin.site.register(Budget)
admin.site.register(AccountTransaction)
admin.site.register(BudgetTransaction)