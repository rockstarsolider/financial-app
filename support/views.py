from django.views import View  
from django.views.generic import TemplateView
from .forms import ContactUsForm, ChatMessageForm, TicketForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import ChatMessage, Forum, ForumMessage, Announcement, TicketCategory
from django.http import HttpResponse
from django.db.models import Max, Min
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404  
from django.core.exceptions import ValidationError  
from django.core.validators import FileExtensionValidator
from tracker.models import CustomUser
from custom_translate.templatetags.persian_calendar_convertor import format_persian_datetime, convert_to_persian_calendar

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
        chat_list = (  
            ChatMessage.objects.values('room_name')
            .annotate(  
                latest_message_timestamp=Max('timestamp'),  
                oldest_message_timestamp=Min('timestamp')  
            )
        )
        for chat in chat_list:  
            chat['latest_message_timestamp'] = format_persian_datetime(convert_to_persian_calendar(chat['latest_message_timestamp']))  
            chat['oldest_message_timestamp'] = format_persian_datetime(convert_to_persian_calendar(chat['oldest_message_timestamp'])) 
        return render(request, 'support/chat_list.html', {'chat_list': chat_list })
    
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
            messages.error(request, 'شما بلاک شده اید و نمیتوانید پیامی ارسال کنید')
            return render(request, 'partial/message.html', {'error': True})
        message_text = request.POST.get('message') 
        attachment = request.FILES.get('attachment')
        if attachment:  
            try:  
                FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])(attachment)  
            except ValidationError as e:  
                messages.error(request, 'فایل های مجاز: png, jpg, jpeg, webp')  
                return render(request, 'partial/message.html', {'error':True})
        if message_text.strip() or attachment:  
            forum = Forum.objects.get(name=forum_name)  
            ForumMessage.objects.create(user=request.user, forum=forum, message=message_text, attachment=attachment)
        
        return render(request, 'partial/message.html')
    
    def delete(self, request, message_id):  
        message = get_object_or_404(ForumMessage, id=message_id)  
        message.delete()
        messages.success(request, 'پیام با موفقیت حذف شد')  
        return render(request, 'partial/message.html', {'error':True})
    
class BlockUserView(View):  
    def post(self, request, user_id):  
        user = get_object_or_404(CustomUser, id=user_id)  
        user.blocked = True
        user.save()  
        messages.success(request, 'کاربر با موفقیت بلاک شد')
        return render(request, 'partial/message.html', {'error':True})
    
class TicketView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'support/ticket.html', {'form': TicketForm()})
    
    def post(self, request):
        form = TicketForm(request.POST)  
        attachment = request.FILES.get('attachment')
        if form.is_valid():
            ticket = form.save(commit=False)  
            category_user = form.cleaned_data['category'].user
            print(category_user)
            ticket.support_agent = request.user
            if attachment:
                ticket.attachment = attachment
            ticket.save()
            messages.success(self.request, 'فرم با موفقیت ثبت شد')
            category_user.email_user(
                f'مشکل در بخش {form.cleaned_data['category']}',
                f'یک تیکت توسط پشتیبان با ایمیل {request.user} ساخته شده',
                'admin@gmail.com',
                fail_silently = False
            )
            Announcement.objects.create(
                title=f'مشکل در بخش {form.cleaned_data['category']}', 
                text=f'یک تیکت توسط پشتیبان با ایمیل {request.user} ساخته شده',
                target_user = category_user
            )
            return render(request, 'support/ticket.html',{'form': TicketForm()})
        messages.error(self.request, 'فرم ثبت نشد!')
        return render(request, 'support/ticket.html',{'form': form})