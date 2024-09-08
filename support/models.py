from django.db import models
from tracker.models import CustomUser
from custom_translate.templatetags.persian_calendar_convertor import convert_to_persian_calendar, format_persian_date, format_persian_datetime, convert_to_persian_calendar_date

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