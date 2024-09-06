from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth import login,logout  
from .forms import CustomUserCreationForm, TransactionForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Transaction
from .filters import TransactionFilter
from django_htmx.http import retarget
from django.core.paginator import Paginator
from django.conf import settings
from tracker.charting import income_expense_chart, category_chart
from .resources import TransactionResource
from django.http import HttpResponse
from django.contrib import messages

class RegisterView(generic.CreateView):  
    form_class = CustomUserCreationForm  
    template_name = 'registration/register.html'  
    success_url = reverse_lazy('login') 

    def form_valid(self, form):  
        user = form.save()  
        login(self.request, user)
        return super().form_valid(form)
    
class CustomLoginView(LoginView):  
    template_name = 'registration/login.html'

    def form_valid(self, form):  
        user = form.get_user()  
        login(self.request, user)  
        message = 'کاربر عزیز خوش آمدید'
        if user.first_name:
            message = f'{user.first_name} عزیز خوش آمدی '
        messages.success(self.request, message)  
        return render(self.request, 'tracker/home.html')
    
class CustomLogoutView(View):  
    def get(self, request, *args, **kwargs):  
        logout(request)
        return redirect('logout_confirm')
    
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tracker/home.html', {})
    
class TransactionsList(LoginRequiredMixin,View):
    def get(self, request):
        transactions_filter = TransactionFilter(
            request.GET,
            queryset=Transaction.objects.filter(user=request.user)
        )
        paginator = Paginator(transactions_filter.qs, settings.PAGE_SIZE)
        transaction_page = paginator.page(1)
        total_income = transactions_filter.qs.getTotalIncome()
        total_expenses = transactions_filter.qs.getTotalExpenses()
        net_income = transactions_filter.qs.getNetIncome()
        context = {
            'count':transactions_filter.qs.count(),
            'transactions':transaction_page,
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
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            transaction.save()
            context = {'message':'تراکنش با موفقیت ویرایش شد! '}
            return render(request, 'partial/transaction_success.html', context)
        else:
            context = {
                'form':form,
                'transaction': transaction
            }
            response = render(request, 'partial/update_transaction.html',context)
            return retarget(response, '#transaction-block')

    context = {
        'form':TransactionForm(instance=transaction),
        'transaction': transaction
    }
    return render(request, 'partial/update_transaction.html',context)

@require_http_methods(['DELETE'])
def DeleteTransaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {'message':'تراکنش با موفقیت حذف شد!'}
    return render(request, 'partial/delete_success.html', context)

def GetTransactions(request):
    page = request.GET.get('page', 1)
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user)
    )
    paginator = Paginator(transactions_filter.qs, settings.PAGE_SIZE)
    context = {'transactions':paginator.page(page)}
    return render(request, 'partial/transactions_countainer.html#transaction_list', context)

def TransactionsCharts(request):
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    income_expense_bar = income_expense_chart(transactions_filter.qs)
    category_income_pie = category_chart(transactions_filter.qs.filter(type='income'), 'درآمد بر اساس دسته بندی')
    category_expense_pie = category_chart(transactions_filter.qs.filter(type='expense'), 'مخارج بر اساس دسته بندی')
    context = { 
        'filter': transactions_filter,
        'income_expense_bar': income_expense_bar.to_html(),
        'category_income_pie': category_income_pie.to_html(),
        'category_expense_pie': category_expense_pie.to_html(),
    }
    if request.htmx:
        return render(request, 'partial/charts_container.html', context)
    return render(request, 'tracker/charts.html', context)

def Export(request):
    if request.htmx:
        return HttpResponse(headers={'HX-Redirect':request.get_full_path()})
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    data = TransactionResource().export(transactions_filter.qs)
    response = HttpResponse(data.json)
    response['Content-Diposition'] = 'attachment; filename="transactions.json"'
    return response