from django.contrib import admin
from .models import ContactUs, Announcement, ChatMessage

# Register your models here.
admin.site.register(ContactUs)
admin.site.register(Announcement)
admin.site.register(ChatMessage)