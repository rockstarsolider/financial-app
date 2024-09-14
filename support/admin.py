from django.contrib import admin
from .models import ContactUs, Announcement, ChatMessage

# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'message', 'timestamp']

admin.site.register(ContactUs)
admin.site.register(Announcement)
admin.site.register(ChatMessage, ChatMessageAdmin)