from django.views import View  
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import ContactUsForm, ChatMessageForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ChatMessage, Forum, ForumMessage
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from django.shortcuts import redirect
from django.utils import timezone

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
            return redirect('home') 
        messages.warning(self.request, 'برای ارتباط با ما ابتدا وارد شوید')  
        return render(request, 'support/contact_us.html', {'form': form})
    
class ChatRoomView(LoginRequiredMixin, TemplateView):  
    template_name = 'support/chat_room.html'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        room_name = kwargs.get('room_name')  
        messages = ChatMessage.objects.filter(room_name=room_name)  
        form = ChatMessageForm() 
        context['room_name'] = room_name
        context['messages'] = messages  
        context['email'] = self.request.user.email
        context['username'] = self.request.user.email
        context['user_type'] = self.request.user.user_type
        context['form'] = form
        return context
    def post(self, request, **kwargs):
        room_name = kwargs.get('room_name')  
        form = ChatMessageForm(request.POST, request.FILES)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.room_name = room_name
            chat_message.user = request.user
            chat_message.save()
            return redirect('chat_room', room_name=room_name)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

class ChatListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self): 
        return self.request.user.user_type == 'support'
    def handle_no_permission(self):  
        return HttpResponse(status=204, headers={'HX-Redirect': 'login'})
    
    def get(self, request):
        latest_messages = (ChatMessage.objects.values('room_name').annotate(latest_timestamp=Max('timestamp')))  
        unique_rooms = ChatMessage.objects.filter(  timestamp__in=[msg['latest_timestamp'] for msg in latest_messages]  ) 
        return render(request, 'support/chat_list.html', {'rooms': unique_rooms})
    
class ForumView(LoginRequiredMixin, View):
    def get(self, request, forum_name):  
        if not request.user.has_premium:  
            return redirect('home')
        forum = Forum.objects.get(name=forum_name)  
        forums = Forum.objects.all()
        messages = ForumMessage.objects.filter(forum=forum)  
        
        return render(request, 'support/forum.html', {  
            'forum': forum,  
            'messages': messages,  
            'forums':forums
        })

class ForumMessageView(LoginRequiredMixin, View):  
    def post(self, request, forum_name):    
        if request.user.blocked:  
            messages.error('شما بلاک شده اید و نمیتوانید پیامی ارسال کنید')
            return render(request, 'support/forum.html', {})
        message_text = request.POST.get('message')  
        if message_text.strip():  
            forum = Forum.objects.get(name=forum_name)  
            ForumMessage.objects.create(user=request.user, forum=forum, message=message_text)
        
        return render(request, 'partial/message.html', {
            'message': message_text,
            'username': request.user.email,
            'timestamp': timezone.now().isoformat(),
        })