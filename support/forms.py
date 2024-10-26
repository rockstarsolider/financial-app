from django import forms  
from .models import ContactUs, ChatMessage, Ticket

class ContactUsForm(forms.ModelForm):  
    title = forms.CharField(required=True, max_length=40, label='عنوان')
    text = forms.CharField(required=True, widget=forms.Textarea, label='متن')

    class Meta:  
        model = ContactUs  
        fields = ['title', 'text'] 

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'پیام را بنویسید'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'category', 'attachment']