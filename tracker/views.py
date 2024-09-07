from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth import login,logout  
from .forms import CustomUserCreationForm, TransactionForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Transaction, Category
from .filters import TransactionFilter
from django.core.paginator import Paginator
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
    
class TransactionView(LoginRequiredMixin, View):  
    def get(self, request, pk=None):  
        if pk:  # updating or viewing a transaction  
            transaction = get_object_or_404(Transaction, pk=pk, user=request.user)  
            form = TransactionForm(instance=transaction)  
            context = {'form': form, 'transaction': transaction}  
            return render(request, 'partial/update_transaction.html', context)  

        # listing transactions  
        transactions_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user))  
        paginator = Paginator(transactions_filter.qs, 5)  
        transaction_page = paginator.page(1)  
        context = {  
            'count': transactions_filter.qs.count(),  
            'transactions': transaction_page,  
            'filter': transactions_filter,  
            'total_income': transactions_filter.qs.getTotalIncome(),  
            'total_expenses': transactions_filter.qs.getTotalExpenses(),  
            'net_income': transactions_filter.qs.getNetIncome()  
        }  
        if request.htmx:  
            return render(request, 'partial/transactions_countainer.html', context)  
        return render(request, 'tracker/transactions_list.html', context)  

    def post(self, request, pk=None):  # Update transaction  
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)  
        form = TransactionForm(request.POST, instance=transaction)  
        if form.is_valid():  
            new_category_name = form.cleaned_data.get('new_category')  
            if new_category_name:  
                category, created = Category.objects.get_or_create(name=new_category_name)  
                form.instance.category = category
            transaction = form.save(commit=False)  
            transaction.user = request.user  
            transaction.save()  
            context = {'message': 'تراکنش با موفقیت تغییر کرد !'}  
            return render(request, 'partial/delete_success.html', context)  
        else:  
            context = {'form': form}  
            return render(request, 'partial/create_transaction.html', context)  

    def delete(self, request, pk):  
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)  
        transaction.delete()  
        context = {'message': 'تراکنش با موفقیت حذف شد!'}  
        return render(request, 'partial/delete_success.html', context)  
    
def CreateTransaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        new_category_name = form.cleaned_data.get('new_category')  
        if new_category_name:  
            category, created = Category.objects.get_or_create(name=new_category_name)  
            form.instance.category = category
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        context = {'message':'تراکنش با موفقیت اضافه شد! '}
        return render(request, 'partial/transaction_success.html', context)
    else:
        context = {'form':form}
        return render(request, 'partial/create_transaction.html', context)

def GetTransactions(request):
    page = request.GET.get('page', 1)
    transactions_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user))
    paginator = Paginator(transactions_filter.qs, 5)
    context = {'transactions':paginator.page(page)}
    return render(request, 'partial/transactions_countainer.html#transaction_list', context)

def TransactionsCharts(request):
    transactions_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).select_related('category'))
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
    transactions_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(user=request.user).select_related('category'))
    data = TransactionResource().export(transactions_filter.qs)
    response = HttpResponse(data.json)
    response['Content-Diposition'] = 'attachment; filename="transactions.json"'
    return response