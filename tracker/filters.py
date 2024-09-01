from .models import Transaction, Category
import django_filters
from django import forms

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        empty_label = 'همه',
        field_name = 'type',
        lookup_expr = 'iexact', 
        label='نوع تراکنش'
    )

    start_date = django_filters.DateFilter(
        field_name = 'date',
        lookup_expr = 'gte',
        label = 'از تاریخ',
        widget = forms.DateInput(attrs={'type':'date'},),
    )

    end_date = django_filters.DateFilter(
        field_name = 'date',
        lookup_expr = 'lte',
        label = 'تا تاریخ',
        widget = forms.DateInput(attrs={'type':'date'},),
    )

    category = django_filters.ModelMultipleChoiceFilter(
        queryset = Category.objects.all(),
        widget = forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type','start_date', 'end_date','category',)