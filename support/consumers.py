from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import get_template

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

    def user_logged_in(self, event):
        html = get_template('partial/notification.html').render(
            context={'text': event['text']}
        )
        self.send(text_data=html)
    
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