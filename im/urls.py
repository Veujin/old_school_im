from django.urls import path
from . import views

app_name = 'im'
urlpatterns = [
    path('chats', views.ChatsView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>', views.ChatMessagesView.as_view(), name='chat')
]