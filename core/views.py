from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, FormView, CreateView, FormView
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

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
         view = HomeListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        action = self.request.POST['action']

        if (action == 'btn-acct'):
            account_form = AddAccountForm(request.POST)
            if account_form.is_valid():
                name = account_form.cleaned_data.get('name')
                if Account.objects.filter(name=name, username=self.request.user).exists():
                    messages.error(request, f"The account name you entered already exists.")
                    return redirect(reverse('home'))
                else:
                    view = AddAccount.as_view()
                
        elif (action == 'btn-trans'):
            transaction_form = AddAccountTransactionForm(self.request.user, request.POST)
            if transaction_form.is_valid():
                view = AddAccountTransaction.as_view()
        elif(action == 'btn-transf'):
            tranfer_form = MakeTransferForm(self.request.user, request.POST)
            if tranfer_form.is_valid():
                view = MakeTransfer.as_view()
                
        return view(request, *args, **kwargs) 


class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'acctrans_list'
    
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
        accounts = Account.objects.filter(username = self.request.user).values('name' ,'balance').order_by('-balance')
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

        if (action == 'btn-budg'):
            budget_form = AddBudgetForm(self.request.user, request.POST)
            if budget_form.is_valid():
                view = AddBudget.as_view()
                
        elif (action == 'btn-trans'):
            transaction_form = AddBudgetTransactionForm(self.request.user, request.POST)
            if transaction_form.is_valid():
                view = AddBudgetTransaction.as_view()
                
        return view(request, *args, **kwargs) 

class BudgetListView(ListView):
    template_name = 'budget.html'
    context_object_name = 'budgtrans_list'
    
    def get_queryset(self):
        return BudgetTransaction.objects.filter(budget__account__username = self.request.user).order_by('-date')
     
    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        
        context = super(BudgetListView, self).get_context_data(**kwargs)
        context['form_budget'] = AddBudgetForm(current_user = self.request.user)
        context['form_transaction'] = AddBudgetTransactionForm(current_user = self.request.user)
        total_balance = AccountTransaction.objects.filter(account__username = self.request.user, trans_type = 'Transfer').values('budget__name', 'trans_type').annotate(total = Sum('amount'))
        budget_expenses = BudgetTransaction.objects.filter(budget__account__username = self.request.user).values('budget', 'budget__name', 'budget__balance').annotate(total_expenses = Sum('amount')).order_by('-budget__balance')

        budget_list = []
        
        for b in budget_expenses:
            i = b.get('budget__balance')
            for t in total_balance:
                total = 0
                if not t.get('trans_type'):
                    total = b.get('budget__balance')
                else:
                    if t.get('budget__name') == b.get('budget__name'):
                        i = i + t.get('total') - b.get('total_expenses')
                    total+=i
                b['total_balance'] = total 
                            
            budget_list.append(b)
            
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

class AddAccountTransaction(CreateView):
    model = AccountTransaction
    fields = ['date', 'account', 'trans_type', 'desc', 'amount']

    def get_success_url(self):  
        return reverse('home')       

class MakeTransfer(CreateView):
    model = AccountTransaction
    fields = '__all__'

    def get_success_url(self):  
        return reverse('home') 

class AddBudget(CreateView):
    model = Budget
    fields = ['name', 'account']

    def get_success_url(self):  
        return reverse('budget')

class AddBudgetTransaction(CreateView):
    model = BudgetTransaction
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('budget')