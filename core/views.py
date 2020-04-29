from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Account, Transaction
from .forms import AddAccountForm, AddTransactionForm
from django.views import View
from django.urls import reverse

class HomeView(View):
    def get(self, request, *args, **kwargs):
         view = HomeListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form_account = AddAccountForm(request.POST)
            form_transaction = AddTransactionForm(request.POST)

            if form_account.is_valid():
                view = AddAccount.as_view()
            elif form_transaction.is_valid():
                view = AddTransaction.as_view()

        return view(request, *args, **kwargs) 

class HomeListView(ListView):
    template_name = 'home.html'
    context_object_name = 'account_list'
    queryset = Account.objects.all().order_by('-balance')

    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['form_account'] = AddAccountForm()
        context['form_transaction'] = AddTransactionForm()
        context['trans_list'] = Transaction.objects.all().order_by('-date')
        return context

class AddAccount(CreateView):
    form_class = AddAccountForm
    
    def get_success_url(self):
        return reverse('home')

class AddTransaction(CreateView):
    form_class = AddTransactionForm
    
    def get_success_url(self):
        return reverse('home')