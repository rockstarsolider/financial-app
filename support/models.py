from django.db import models
from tracker.models import CustomUser

# Create your models here.
class ContactUs(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    title = models.CharField(max_length=40, verbose_name='عنوان')
    text = models.TextField(null=True, blank=True, verbose_name='متن')
    def __str__(self):
        return f'{self.user.email} : {self.title}'