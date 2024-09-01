from django import forms  
from .models import CustomUser, Transaction, Category

class CustomUserCreationForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:  
        model = CustomUser  
        fields = ('email', 'password', 'first_name', 'last_name')  

    def save(self, commit=True):  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data['password']) 
        if commit:  
            user.save()  
        return user  
    
class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget = forms.RadioSelect(),
    )
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("مقدار باید یک عدد مثبت باشد")
        return amount
    class Meta:
        model = Transaction
        fields = (
            'type',
            'amount',
            'date',
            'category',
        )
        widgets = {
            'date': forms.DateInput(attrs={'type':'date'}),
        }