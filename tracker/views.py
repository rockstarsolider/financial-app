from django.urls import reverse_lazy  
from django.views import generic  
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout  
from django.shortcuts import redirect 
from django.views import View
from django.shortcuts import render
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_datetime
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Transaction

class RegisterView(generic.CreateView):  
    form_class = CustomUserCreationForm  
    template_name = 'registration/register.html'  
    success_url = reverse_lazy('login')  

    def form_valid(self, form):  
        user = form.save()  
        login(self.request, user)
        return super().form_valid(form)
    
class CustomLogoutView(View):  
    def get(self, request, *args, **kwargs):  
        logout(request)
        return redirect('logout_confirm')
    
class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context.update({'joined':format_persian_datetime(convert_to_persian_calendar(request.user.date_joined))})
        return render(request, 'tracker/home.html', context)
    
class TransactionsList(LoginRequiredMixin,View):
    def get(self, request):
        transactions = Transaction.objects.filter(user = request.user)
        context = {
            'transactions':transactions,
            }
        return render(request, 'tracker/transactions_list.html', context)