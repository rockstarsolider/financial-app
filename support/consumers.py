from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template
import json  
from .models import ChatMessage
from channels.db import database_sync_to_async
from tracker.models import CustomUser

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            self.close()
            return
        self.GROUP_NAME = 'user-notifications'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.GROUP_NAME, self.channel_name
            )
    
    def new_announcement(self, event):  
        html = get_template('partial/notification.html').render(  
            context={
                'title': event['title'],
                'text': event['text'],
                'persian_date': event['persian_date'],
                'pk': event['pk'],
            }  
        )  
        self.send(text_data=html)

class ChatConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        self.room_name = self.scope['url_route']['kwargs']['room_name']  
        self.room_group_name = f'chat_{self.room_name}'  

        # Join room group  
        await self.channel_layer.group_add(  
            self.room_group_name,  
            self.channel_name  
        )  

        await self.accept()  

    async def disconnect(self, close_code):  
        # Leave room group  
        await self.channel_layer.group_discard(  
            self.room_group_name,  
            self.channel_name  
        )  

    async def receive(self, text_data):  
        text_data_json = json.loads(text_data)  
        message = text_data_json['message']  
        username = text_data_json['username']
        user_type = text_data_json['user_type']

        # Save message in the database  
        user = await database_sync_to_async(CustomUser.objects.get)(email=username)
        chat_message = ChatMessage(room_name=self.room_name, user=user, message=message)  
        await database_sync_to_async(chat_message.save)()

        # Send message to room group  
        await self.channel_layer.group_send(  
            self.room_group_name,  
            {  
                'type': 'chat_message',  
                'message': message,  
                'username': username,
                'user_type': user_type
            }  
        )  

    async def chat_message(self, event):  
        message = event['message']  
        username = event['username']  
        user_type = event['user_type']
        attachment = event['attachment']

        # Send message to WebSocket  
        await self.send(text_data=json.dumps({  
            'message': message,  
            'username': username,
            'user_type': user_type,
            'attachment': attachment
        }))


class ForumConsumer(AsyncWebsocketConsumer):  
    async def connect(self):  
        self.forum_name = self.scope['url_route']['kwargs']['forum_name']  
        self.room_group_name = f'forum_{self.forum_name}'  

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  

        await self.accept()  

    async def disconnect(self, close_code):  
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  

    async def receive(self, text_data):  
        data = json.loads(text_data)  
        message = data['message']  
        email = data['email']  
        
        await self.channel_layer.group_send(  
            self.room_group_name,  
            {  
                'type': 'forum_message',  
                'message': message,  
                'email': email,  
            }  
        )  

    async def forum_message(self, event):  
        message = event['message']  
        email = event['email']  

        # Send message to WebSocket  
        await self.send(text_data=json.dumps({  
            'message': message,  
            'email': email,  
        }))  