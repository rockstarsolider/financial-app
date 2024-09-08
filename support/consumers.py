from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template
import json  

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
    

class ChatConsumer(WebsocketConsumer):  
    def connect(self):  
        self.user = self.scope['user']  
        if not self.user.is_authenticated:  
            self.close()  
            return  
        
        self.group_name = 'support_chat'  
        async_to_sync(self.channel_layer.group_add)(  
            self.group_name, self.channel_name  
        )  
        self.accept()  

    def disconnect(self, close_code):  
        if self.user.is_authenticated:  
            async_to_sync(self.channel_layer.group_discard)(  
                self.group_name, self.channel_name  
            )  

    def receive(self, text_data):  
        text_data_json = json.loads(text_data)  
        message = text_data_json['message']  
        
        # Broadcast the message to the group  
        async_to_sync(self.channel_layer.group_send)(  
            self.group_name,  
            {  
                'type': 'chat_message',  
                'message': message,  
                'user': self.user.email,  
            }  
        )  

    def chat_message(self, event):  
        message = event['message']  
        user = event['user']
        
        self.send(text_data=json.dumps({  
            'message': message,  
            'user': user,
            'current_user':self.user.email
        }))  