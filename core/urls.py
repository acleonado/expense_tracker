from django.contrib import admin
from django.urls import path
from .views import HomeView, BudgetView, AccountDeleteView

urlpatterns = [
    path('account/', HomeView.as_view(), name = 'home'),
    path('budget/', BudgetView.as_view(), name = 'budget'),
]
