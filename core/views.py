from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView
from .models import Account
from .forms import AddAccountForm
from django.views import View
from django.urls import reverse

class HomeView(View):
    def get(self, request, *args, **kwargs):
         view = AccountListView.as_view()
         return view(request, *args, **kwargs) 

    def post(self, request, *args, **kwargs):
         view = AddAccount.as_view()
         return view(request, *args, **kwargs) 

class AccountListView(ListView):
    model = Account
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # This is frequently used to pass all kinds of data to a template. 
        # The template can then render these components accordingly.
        context = super().get_context_data(**kwargs)
        context['form'] = AddAccountForm()
        return context

    def get_queryset(self):
        return Account.objects.all().order_by('-balance')

class AddAccount(CreateView):
    form_class = AddAccountForm
    # success_message = "Successfully registered to %(title)s Event"

    # def get_success_message(self, cleaned_data):
    #     return self.success_message % dict(
    #         cleaned_data,
    #         title=self.object.event_id.title,
    #     )
    def get_success_url(self):
        return reverse('home')