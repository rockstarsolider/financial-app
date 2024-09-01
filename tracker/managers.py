from django.db import models

class TransactionQuerySet(models.QuerySet):
    def get_expenses(self):
        return self.filter(type='expense')
    
    def get_income(self):
        return self.filter(type='income')
    
    def getTotalExpenses(self):
        return f'{self.get_expenses().aggregate(total=models.Sum('amount'))['total'] or 0 :,} تومان '

    def getTotalIncome(self):
        return f'{self.get_income().aggregate(total=models.Sum('amount'))['total'] or 0:,} تومان '
    
    def getNetIncome(self):
        total_income = self.get_income().aggregate(total=models.Sum('amount'))['total'] or 0
        total_expenses = self.get_expenses().aggregate(total=models.Sum('amount'))['total'] or 0
        return (f'{total_income - total_expenses:,} تومان ')