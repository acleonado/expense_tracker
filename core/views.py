from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, FormView, CreateView, DeleteView, UpdateView
from .models import Account, AccountTransaction, Budget, BudgetTransaction
from .forms import AddAccountForm, AddBudgetForm, AddAccountTransactionForm, AddBudgetTransactionForm, MakeTransferForm
from django.views import View
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
         view = HomeListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        action = self.request.POST['action']

        if action == 'btn-acct':
            account_form = AddAccountForm(request.POST)
            if account_form.is_valid():
                name = account_form.cleaned_data.get('name')
                if Account.objects.filter(name=name, username=self.request.user).exists():
                    messages.error(request, f"The account name you entered already exists.")
                    return redirect(reverse('home'))
                else:
                    view = AddAccount.as_view()
        elif action == 'btn-edit-acct':
            account_form = AddAccountForm(request.POST)
            if account_form.is_valid():
                name = account_form.cleaned_data.get('name')
                if Account.objects.filter(name=name, username=self.request.user).exists():
                    messages.error(request, f"The account name you entered already exists.")
                    return redirect(reverse('home'))
                else:
                    view = EditAccount.as_view()
        elif action == 'btn-trans':
            transaction_form = AddAccountTransactionForm(self.request.user, request.POST)
            if transaction_form.is_valid():
                view = AddAccountTransaction.as_view()
        elif action == 'btn-transf':
            tranfer_form = MakeTransferForm(self.request.user, request.POST)
            if tranfer_form.is_valid():
                view = MakeTransfer.as_view()
        elif action == 'btn-acct-del':
            view = AccountDeleteView.as_view()
        elif action == 'btn-acct-trans-del':
            view = AccountTransactionDeleteView.as_view()
        elif action == 'btn-make-transf-del':
            view = TransferDeleteView.as_view()
            

        return view(request, *args, **kwargs) 


class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'acctrans_list'
    paginate_by = 15
    
    def get_queryset(self):
        return AccountTransaction.objects.filter(account__username = self.request.user).exclude(trans_type = 'Transfer').order_by('-date')
     
    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['form_account'] = AddAccountForm()
        context['form_transaction'] = AddAccountTransactionForm(current_user = self.request.user)
        context['form_transfer'] = MakeTransferForm(current_user = self.request.user)
        context['transfer_list'] = AccountTransaction.objects.filter(account__username = self.request.user, trans_type = 'Transfer').order_by('-date')

        accounts = Account.objects.filter(username = self.request.user).values('id', 'name' ,'balance').order_by('name')
        total_balance = Account.objects.filter(username = self.request.user).values('name', 'accounttransaction__trans_type').annotate(total = Sum('accounttransaction__amount'))
        
        account_list = []
        
        for a in accounts:
            i = a.get('balance')
            for t in total_balance:
                total = 0
                if t.get('name') == a.get('name'):
                    if not t.get('accounttransaction__trans_type'):
                        total = a.get('balance')
                    else:
                        if t.get('accounttransaction__trans_type') == 'Income':
                            i = i + t.get('total')
                        elif t.get('accounttransaction__trans_type') == 'Transfer':
                            i =  i - t.get('total')
                        elif t.get('accounttransaction__trans_type') == 'Expense':
                            i = i - t.get('total')
                        
                        total+=i
                    a['total_balance'] = total
                    
            account_list.append(a)
            
        context['account_list'] = account_list

        return context

class BudgetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
         view = BudgetListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        action = self.request.POST['action']

        if action == 'btn-budg':
            budget_form = AddBudgetForm(self.request.user, request.POST)
            if budget_form.is_valid():
                name = budget_form.cleaned_data.get('name')
                if Budget.objects.filter(name=name, account__username=self.request.user).exists():
                    messages.error(request, f"The budget name you entered already exists.")
                    return redirect(reverse('budget'))
                else:
                    view = AddBudget.as_view()
        elif action == 'btn-trans':
            transaction_form = AddBudgetTransactionForm(self.request.user, request.POST)
            if transaction_form.is_valid():
                view = AddBudgetTransaction.as_view()
        elif action == 'btn-edit-budget':
            budget_form = AddBudgetForm(self.request.user, request.POST)
            if budget_form.is_valid():
                name = budget_form.cleaned_data.get('name')
                if Budget.objects.filter(name=name, account__username=self.request.user).exists():
                    messages.error(request, f"The budget name you entered already exists.")
                    return redirect(reverse('budget'))
                else:
                    view = EditBudget.as_view()
        elif action == 'btn-budget-del':
            view = BudgetDelete.as_view()    

        return view(request, *args, **kwargs) 

class BudgetListView(ListView):
    template_name = 'budget.html'
    context_object_name = 'budgtrans_list'
    paginate_by = 20
    
    def get_queryset(self):
        return BudgetTransaction.objects.filter(budget__account__username = self.request.user).order_by('-date')
     
    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        
        context = super(BudgetListView, self).get_context_data(**kwargs)
        context['form_budget'] = AddBudgetForm(current_user = self.request.user)
        context['form_transaction'] = AddBudgetTransactionForm(current_user = self.request.user)
        transfer_balance = AccountTransaction.objects.filter(account__username = self.request.user, trans_type = 'Transfer').values('budget__id', 'budget__name', 'trans_type').annotate(total = Sum('amount'))
        budget_expenses = BudgetTransaction.objects.filter(budget__account__username = self.request.user).values('budget__id', 'budget__name', 'budget__balance').annotate(total_expenses = Sum('amount'))
        budgets = Budget.objects.filter(account__username = self.request.user).values('id','name', 'account', 'balance').order_by('name')

        budget_list = []
        for budget in budgets:
            i = budget.get('balance')
            for b in budget_expenses:
                for t in transfer_balance:
                    total = 0
                    if BudgetTransaction.objects.filter(budget__account__username = self.request.user, budget = t.get('budget__id')).exists():
                         # if the budget name exists in the budget transaction and account transaction table, execute if statement
                        if t.get('budget__name') == budget.get('name') and b.get('budget__name') == t.get('budget__name'):
                            # if all budget names are equal to the budget name of budget transaction and account transaction table, then
                            # add the default balance to the total amount transfered and subtract the total expenses from budget transaction table
                            i = i + t.get('total') - b.get('total_expenses')
                    else:
                        if AccountTransaction.objects.filter(account__username = self.request.user, trans_type = 'Transfer', budget = budget.get('id')).exists():
                            # if budget name does not exist in budget transaction but exists in account transaction, execute if statement
                            if t.get('budget__name') == budget.get('name'):
                                # if the budget name is equal to the budget name from the account transaction, then 
                                # add the balance to the total transfered amount from account transaction table
                                total = budget.get('balance') + t.get('total')
                        elif BudgetTransaction.objects.filter(budget__account__username = self.request.user, budget = b.get('budget__id')).exists():
                            # if budget name does not exists in account transaction table but exists in budget transaction table, execute if statement
                            if b.get('budget__name') == budget.get('name'):
                                # if the budget name is equal to the budget name from the budget transaction, then 
                                # subtract the budget balance to the total expenses from the budget transaction table. 
                                # this will result to a negative amount bec the default balance is $0 and no amount is transfered yet to this budget account
                                i = i - b.get('total_expenses')

                    total+=i
                    budget['total_balance'] = total 
            budget_list.append(budget)
        context['budget_list'] = budget_list     
        return context

class AddAccount(CreateView):
    model = Account
    fields = ['name', 'balance']

    def form_valid(self, form_account):
        form_account.instance.username = self.request.user
        return super().form_valid(form_account)

    def get_success_url(self):  
        return reverse('home')

class AccountDeleteView(DeleteView):
    model = Account

    def get_object(self):
        id_ = self.request.POST.get('name')
        return get_object_or_404(Account, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Account Successfully Deleted!")
        return reverse('home')

class EditAccount(UpdateView):
    model = Account
    fields = ['name', 'balance']

    def get_object(self):
        id_ = self.request.POST.get('id')
        return get_object_or_404(Account, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Account Successfully Updated!")
        return reverse('home')

class AddAccountTransaction(CreateView):
    model = AccountTransaction
    fields = ['date', 'account', 'trans_type', 'desc', 'amount']
    
    def get_success_url(self):  
        return reverse('home') 

class AccountTransactionDeleteView(DeleteView):
    model = AccountTransaction

    def get_object(self):
        id_ = self.request.POST.get('id')
        return get_object_or_404(AccountTransaction, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Account Transaction Successfully Deleted!")
        return reverse('home')      

class MakeTransfer(CreateView):
    model = AccountTransaction
    fields = '__all__'

    def get_success_url(self):  
        return reverse('home') 

class TransferDeleteView(DeleteView):
    model = AccountTransaction

    def get_object(self):
        id_ = self.request.POST.get('id')
        return get_object_or_404(AccountTransaction, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Transfer Successfully Cancelled!")
        return reverse('home')    

class AddBudget(CreateView):
    model = Budget
    fields = ['name', 'account']

    def get_success_url(self):  
        return reverse('budget')

class EditBudget(UpdateView):
    model = Budget
    fields = ['name', 'account']

    def get_object(self):
        id_ = self.request.POST.get('id')
        return get_object_or_404(Budget, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Budget Successfully Updated!")
        return reverse('budget')

class BudgetDelete(DeleteView):
    model = Budget

    def get_object(self):
        id_ = self.request.POST.get('id')
        return get_object_or_404(Budget, id=id_)

    def get_success_url(self):
        messages.success(self.request, f"Budget Successfully Deleted!")
        return reverse('budget')

class AddBudgetTransaction(CreateView):
    model = BudgetTransaction
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('budget')

class TransactionDetailView(UpdateView):
    model = AccountTransaction
    form_class = AddAccountTransactionForm
    template_name = 'transaction_detail.html'
     
    def get_form_kwargs(self):
        kwargs = super(TransactionDetailView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs
    
    def get_success_url(self):
        messages.success(self.request, f"Transaction Successfully Updated!")
        return reverse('home')

class TransferDetailView(UpdateView):
    model = AccountTransaction
    form_class = MakeTransferForm
    template_name = 'transfer_detail.html'
     
    def get_form_kwargs(self):
        kwargs = super(TransferDetailView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs
    
    def get_success_url(self):
        messages.success(self.request, f"Transfer Successfully Updated!")
        return reverse('home')