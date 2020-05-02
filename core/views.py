from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Account, Transaction
from .forms import AddAccountForm, AddTransactionForm
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
            form_transaction = AddTransactionForm(request.POST or None)

            if form_account.is_valid():
                view = AddAccount.as_view()
            elif form_transaction.is_valid():
                view = AddTransaction.as_view()

        return view(request, *args, **kwargs) 

class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'trans_list'
    queryset = Transaction.objects.all().order_by('-date')
     

    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['form_account'] = AddAccountForm()
        context['form_transaction'] = AddTransactionForm()
        context['account_list'] = Account.objects.all().order_by('-balance')
        # context['try'] = Transaction.objects.all().select_related('account')
        context['expense'] = Account.objects.values('name', 'transaction__trans_type', 'balance').annotate(sum_expense = Sum('transaction__amount'))
        
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
    form_class = AddTransactionForm
    
    def get_success_url(self):
        return reverse('home')