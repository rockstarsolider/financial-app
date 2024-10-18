from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Announcement, ChatMessage, ForumMessage

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

@receiver(post_save, sender=ChatMessage)  
def chat_message_handler(sender, instance, created, **kwargs):  
    if created:  
        channel_layer = get_channel_layer()  
        async_to_sync(channel_layer.group_send)(  
            f'chat_{instance.room_name}',  
            {  
                'type': 'chat_message',  
                'message': instance.message,  
                'username': instance.user.email,
                'user_type': instance.user.user_type,
                'timestamp': instance.timestamp.isoformat(),
                'attachment': instance.attachment.url if instance.attachment else None,
            }  
        )  

@receiver(post_save, sender=ForumMessage)  
def send_message_to_group(sender, instance, created, **kwargs):  
    if created:  
        channel_layer = get_channel_layer()  
        message_data = {  
            'message': instance.message,  
            'email': instance.user.first_name,  
            'attachment': instance.attachment.url if instance.attachment else None,
        }  
        async_to_sync(channel_layer.group_send)(  
            f'forum_{instance.forum.name}',  # Group name based on the forum  
            {  
                'type': 'forum_message',      # Type for the consumer to handle  
                'message': message_data['message'],  
                'email': message_data['email'],  
                'attachment': message_data['attachment'],
            }  
        ) 