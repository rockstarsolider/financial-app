from django.db import models
from tracker.models import CustomUser
from custom_translate.templatetags.persian_calendar_convertor import format_persian_date, convert_to_persian_calendar_date
from django.core.validators import FileExtensionValidator

class ContactUs(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    title = models.CharField(max_length=40, verbose_name='عنوان')
    text = models.TextField(null=True, blank=True, verbose_name='متن')
    def __str__(self):
        return f'{self.user.email} : {self.title}'

class Announcement(models.Model): 
    title = models.CharField(max_length=25) 
    text = models.TextField()  
    announced_at = models.DateField(auto_now_add=True)

    def __str__(self):  
        return self.title
    
    @property
    def persian_date(self):
        return format_persian_date(convert_to_persian_calendar_date(self.announced_at))

class ChatMessage(models.Model):  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')  
    room_name = models.CharField(max_length=255)  
    message = models.TextField(verbose_name='پیام')  
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='فایل پیوست')
    timestamp = models.DateTimeField(auto_now_add=True)  

    class Meta:  
        ordering = ['timestamp']

class Forum(models.Model):  
    name = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name 

class ForumMessage(models.Model):  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)  
    message = models.TextField()  
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'webp'])])
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'Message by {self.user} at {self.forum}'