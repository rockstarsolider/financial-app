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
    actions = ['set_resolved_action']

    @admin.action(description='تغییر وضعیت تیکت های انتخاب شده به حل شده')
    def set_resolved_action(self, request, queryset):
        queryset.update(is_resolved=True)
        for ticket in queryset:
            user = ticket.support_agent
            user.email_user(
                f'تیکت شماره {ticket.id}',
                f'مشکلی که گزارش کرده بودید با موفقیت حل شد',
                'admin@gmail.com',
                fail_silently = False
            )
            Announcement.objects.create(
                title = f'تیکت شماره {ticket.id}', 
                text = f'مشکلی که گزارش کرده بودید با موفقیت حل شد',
                target_user = user
            )
            self.message_user(
                request,
                'تیکت های انتخاب شده به وضعیت حل شده تغییر یافتند'
            )

admin.site.register(ContactUs)
admin.site.register(TicketCategory, TicketCategoryAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumMessage, ForumMessageAdmin)
admin.site.register(Announcement)
admin.site.register(ChatMessage, ChatMessageAdmin)