from django.contrib import admin
from .models import ContactUs, Announcement, ChatMessage, Forum, ForumMessage, Ticket, TicketCategory

# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'message', 'timestamp']

class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at',]

class ForumMessageAdmin(admin.ModelAdmin):
    list_display = ['forum', 'user', 'created_at',]

class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'support_agent', 'category', 'priority', 'created_at', 'is_resolved']
    search_fields = ['title', 'support_agent', 'category', 'priority']

admin.site.register(ContactUs)
admin.site.register(TicketCategory, TicketCategoryAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumMessage, ForumMessageAdmin)
admin.site.register(Announcement)
admin.site.register(ChatMessage, ChatMessageAdmin)