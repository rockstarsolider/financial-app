from django.urls import path  
from django.contrib.auth import views as auth_views  
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),  
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout_confirm/', TemplateView.as_view(template_name='registration/logout_confirm.html'), name='logout_confirm'),
    path('', views.HomeView.as_view(), name='home'),
    path('transactions/', views.TransactionsList.as_view(), name='transactions'),
    path('transactions/create/', views.TransactionView.as_view(), name='create-transaction'),
    path('transactions/<int:pk>/update/', views.UpdateTransaction, name='update-transaction'),
    path('transactions/<int:pk>/delete/', views.DeleteTransaction, name='delete-transaction'),
    path('get-transactions/', views.GetTransactions, name='get-transactions'),
    path('transactions/charts', views.TransactionsCharts, name='transactions-charts'),
    path('transactions/export', views.Export, name='export'),
]