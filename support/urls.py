from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name='contact-us'),
    path('chat/<str:room_name>/', views.ChatRoomView.as_view(), name='chat_room'),  
    path('chat_list/', views.ChatListView.as_view(), name='chat_list'),  
    path('forum/<str:forum_name>/', views.ForumView.as_view(), name='forum'),  
    path('forum/<str:forum_name>/message/', views.ForumMessageView.as_view(), name='forum_message'), 
]
