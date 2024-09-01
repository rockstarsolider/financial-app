from django.urls import reverse_lazy  
from django.views import generic  
from django.contrib.auth import login
from .forms import CustomUserCreationForm, TransactionForm
from django.contrib.auth import logout  
from django.shortcuts import redirect 
from django.views import View
from django.shortcuts import render, get_object_or_404
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_datetime
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Transaction
from .filters import TransactionFilter

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
        transactions_filter = TransactionFilter(
            request.GET,
            queryset=Transaction.objects.filter(user=request.user)
        )
        total_income = transactions_filter.qs.getTotalIncome()
        total_expenses = transactions_filter.qs.getTotalExpenses()
        net_income = transactions_filter.qs.getNetIncome()
        context = {
            'filter':transactions_filter,
            'total_income':total_income, 
            'total_expenses':total_expenses, 
            'net_income': net_income
        }
        if request.htmx:
            return render(request, 'partial/transactions_countainer.html', context)
        return render(request, 'tracker/transactions_list.html', context)
    
class TransactionView(LoginRequiredMixin,View):
    def get(self, request, pk=None):
        context = {'form':TransactionForm()}
        return render(request, 'partial/create_transaction.html', context)
    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message':'تراکنش با موفقیت اضافه شد! '}
            return render(request, 'partial/transaction_success.html', context)
        else:
            context = {'form':form}
            return render(request, 'partial/create_transaction.html', context)

def UpdateTransaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {
        'form':TransactionForm(instance=transaction),
        'transaction': transaction
    }
    return render(request, 'partial/update_transaction.html',context)