from django.contrib import admin
from django.urls import path
from .views import HomeView
# from . import views

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    # path('', views.home, name = 'home')
]