from django.urls import path
from .views import chats_list_view, chat_view, send_view

app_name = 'im'
urlpatterns = [
    path('', chats_list_view, name='chat-list'),
    path('chat/<int:pk>', chat_view, name='chat'),
    path('chat/<int:chat_id>/send', send_view, name='send')
]