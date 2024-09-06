import plotly.express as px
from django.db.models import Sum
from .models import Category

def income_expense_chart(qs):
    x_values = ['income','expense']

    total_income = qs.filter(type='income').aggregate(
        total=Sum('amount')
    )['total']
    total_expense = qs.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total']

    figure = px.bar(x=x_values, y=[total_income,total_expense])

    return figure

def category_chart(qs, title):
    count_per_category = (
        qs.order_by('category').values('category').annotate(total=Sum('amount'))
    )
    category_pks = count_per_category.values_list('category', flat=True).order_by('category')
    categories = Category.objects.filter(pk__in=category_pks).order_by('pk').values_list('name', flat=True)
    total_amounts = count_per_category.order_by('category').values_list('total', flat=True)

    figure = px.pie(values=total_amounts, names=categories)
    figure.update_layout(title=title)
    return figure