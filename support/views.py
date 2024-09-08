from django.views import View  
from django.shortcuts import render
from .forms import ContactUsForm  
from django.contrib import messages
from django.http import JsonResponse , HttpResponse
from channels.layers import get_channel_layer  
from asgiref.sync import async_to_sync  

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

class ChatView(View):
    def get(self, request):  
        return render(request, 'support/chat.html')
    
    def post(self, request):
        message = request.POST.get('message')  
        user = request.user.email  # Get the current user's email  

        # Broadcast the message to the WebSocket group  
        channel_layer = get_channel_layer()  
        async_to_sync(channel_layer.group_send)(  
            'support_chat',  
            {  
                'type': 'chat_message',  
                'message': message,  
                'user': user,  
            }  
        )  
        return JsonResponse({'status':'success'})