from django.views import View  
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import ContactUsForm  
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ChatMessage
from django.http import HttpResponse
from django.db.models import Max

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
    
class ChatRoomView(LoginRequiredMixin, TemplateView):  
    template_name = 'support/chat_room.html'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        room_name = kwargs.get('room_name')  
        
        messages = ChatMessage.objects.filter(room_name=room_name)  
        context['room_name'] = room_name
        context['messages'] = messages  
        context['username'] = self.request.user.email  # Pass username explicitly  
        context['email'] = self.request.user.email
        context['user_type'] = self.request.user.user_type
        return context

class ChatListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self): 
        return self.request.user.user_type == 'support'
    def handle_no_permission(self):  
        return HttpResponse(status=204, headers={'HX-Redirect': 'login'})
    
    def get(self, request):
        latest_messages = (ChatMessage.objects.values('room_name').annotate(latest_timestamp=Max('timestamp')))  
        unique_rooms = ChatMessage.objects.filter(  timestamp__in=[msg['latest_timestamp'] for msg in latest_messages]  ) 
        return render(request, 'support/chat_list.html', {'rooms': unique_rooms})