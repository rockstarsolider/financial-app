from django.contrib import admin
from .models import CustomUser, Category, Transaction
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_datetime

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)