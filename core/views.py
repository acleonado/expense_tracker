from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Account, AccountTransaction
from .forms import AddAccountForm, AddBudgetForm,AddAccountTransactionForm
from django.views import View
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
         view = HomeListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_account = AddAccountForm(request.POST or None)
            form_transaction = AddAccountTransactionForm(request.POST or None)

            if form_account.is_valid():
                name = form_account.cleaned_data.get('name')
                if Account.objects.filter(name=name, username=self.request.user).exists():
                    messages.error(request, f"Account name you entered already exists.")
                    return redirect(reverse('home'))
                else:
                    view = AddAccount.as_view()
            elif form_transaction.is_valid():
                view = AddTransaction.as_view()

        return view(request, *args, **kwargs) 

class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'acctrans_list'
    
    def get_queryset(self):
        return AccountTransaction.objects.filter(account__username = self.request.user).order_by('-date')
     
    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['form_account'] = AddAccountForm()
        context['form_budget'] = AddBudgetForm(current_user = self.request.user)
        context['form_transaction'] = AddAccountTransactionForm(current_user = self.request.user)
        context['account_list'] = Account.objects.filter(username = self.request.user).order_by('-balance')
        # context['expense'] = Account.objects.values('name', 'accounttransaction__trans_type', 'balance').annotate(sum_expense = Sum('accounttransaction__amount'))
        
        return context

class AddAccount(CreateView):
    model = Account
    fields = ['name', 'balance']

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):  
        return reverse('home')

class AddTransaction(CreateView):
    form_class = AddAccountTransactionForm
    
    def get_success_url(self):
        return reverse('home')