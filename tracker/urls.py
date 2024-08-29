from django.urls import path  
from django.contrib.auth import views as auth_views  
from .views import RegisterView, ProfileView, CustomLogoutView, HomeView
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),  
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Custom logout view  
    path('logout_confirm/', TemplateView.as_view(template_name='tracker/logout_confirm.html'), name='logout_confirm'),  # Custom logout confirmation page  
    path('profile/', ProfileView.as_view(), name='profile'),  
    path('', HomeView.as_view(), name='home'),
]