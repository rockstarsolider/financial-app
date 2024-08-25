from django import forms  
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:  
        model = CustomUser  
        fields = ('email', 'password', 'first_name', 'last_name')  

    def save(self, commit=True):  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving  
        if commit:  
            user.save()  
        return user  