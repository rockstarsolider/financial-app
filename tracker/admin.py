from django.contrib import admin
from .models import CustomUser, Category, Transaction
import django_jalali.admin as jadmin

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'persian_date', 'formated_amount', 'type', 'category']
    search_fields = ['user', 'persian_date', 'formated_amount', 'type', 'category']
    list_filter = ['user', 'date', 'type', 'category']
    

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['date_joined', 'last_login']

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)