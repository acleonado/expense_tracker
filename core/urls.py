from django.contrib import admin
from django.urls import path
from .views import HomeView, BudgetView, TransactionDetailView, TransferDetailView, BudgetTransactionDetailView

urlpatterns = [
    path('account/', HomeView.as_view(), name = 'home'),
    path('budget/', BudgetView.as_view(), name = 'budget'),
    path('account/transaction/<int:pk>/', TransactionDetailView.as_view(), name = 'transaction-detail'),
    path('account/transaction/<int:pk>/update/', TransactionDetailView.as_view(), name = 'transaction-update'),
    path('account/transfer/<int:pk>/', TransferDetailView.as_view(), name = 'transfer-detail'),
    path('budget/transaction/<int:pk>/', BudgetTransactionDetailView.as_view(), name = 'budget-detail'),
    path('budget/transaction/<int:pk>/update/', BudgetTransactionDetailView.as_view(), name = 'budget-update'),
]
