from django.views import View  
from django.shortcuts import render
from .forms import ContactUsForm  
from django.contrib import messages

class ContactUsView(View):  
    def get(self, request):  
        form = ContactUsForm()  
        return render(request, 'support/contact_us.html', {'form': form})  

    def post(self, request):  
        form = ContactUsForm(request.POST)  
        if request.user.is_authenticated:
            contact_us = form.save(commit=False)  
            contact_us.user = request.user
            contact_us.save()
            messages.success(self.request, 'فرم با موفقیت ثبت شد') 
            return render(request, 'tracker/home.html')  
        messages.warning(self.request, 'برای ارتباط با ما ابتدا وارد شوید')  
        return render(request, 'support/contact_us.html', {'form': form})