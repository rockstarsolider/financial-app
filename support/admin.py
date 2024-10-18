from django.contrib import admin
from .models import ContactUs, Announcement, ChatMessage, Forum, ForumMessage

# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'message', 'timestamp']

class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at',]

class ForumMessageAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'created_at',]

admin.site.register(ContactUs)
admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumMessage, ForumMessageAdmin)
admin.site.register(Announcement)
admin.site.register(ChatMessage, ChatMessageAdmin)