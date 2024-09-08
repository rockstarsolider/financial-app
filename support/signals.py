from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Announcement

@receiver(post_save, sender=Announcement)  
def notify_users_on_announcement(sender, instance, created, **kwargs):  
    if created:  
        print(f"New announcement created: {instance.title}") 
        channel_layer = get_channel_layer()  
        group_name = 'user-notifications'  
        event = {  
            'type': 'new_announcement',  
            'title': instance.title,
            'text': instance.text,
            'persian_date': instance.persian_date,
            'pk': instance.pk,
        }  
        async_to_sync(channel_layer.group_send)(group_name, event)  