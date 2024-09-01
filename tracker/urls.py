from django.urls import path  
from django.contrib.auth import views as auth_views  
from .views import RegisterView, CustomLogoutView, HomeView, TransactionsList, TransactionView, UpdateTransaction
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout_confirm/', TemplateView.as_view(template_name='registration/logout_confirm.html'), name='logout_confirm'),
    path('', HomeView.as_view(), name='home'),
    path('transactions/', TransactionsList.as_view(), name='transactions'),
    path('transactions/create/', TransactionView.as_view(), name='create-transaction'),
    path('transactions/<int:pk>/update/', UpdateTransaction, name='update-transaction'),
]