from django.urls import path   
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),  
    path('login/', views.CustomLoginView.as_view(), name='login'),  
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout_confirm/', TemplateView.as_view(template_name='registration/logout_confirm.html'), name='logout_confirm'),
    path('', views.HomeView.as_view(), name='home'),
    path('transactions/', views.TransactionView.as_view(), name='transactions'),
    path('transactions/create/', views.CreateTransaction, name='create-transaction'),
    path('transactions/<int:pk>/update/', views.TransactionView.as_view(), name='update-transaction'),
    path('transactions/<int:pk>/delete/', views.TransactionView.as_view(), name='delete-transaction'),
    path('get-transactions/', views.GetTransactions, name='get-transactions'),
    path('transactions/charts', views.TransactionsCharts, name='transactions-charts'),
    path('transactions/export', views.Export, name='export'),
]