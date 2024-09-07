from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in  
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(user_logged_in)
def send_notifications_on_login(sender, request, user, **kwargs):  
    channel_layer = get_channel_layer()  
    group_name = 'user-notifications'  
    event = {  
        'type': 'user_logged_in',  
        'text': f'{user.email} has logged in.'
    }  
    async_to_sync(channel_layer.group_send)(group_name, event)  