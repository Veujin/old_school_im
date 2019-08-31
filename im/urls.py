from django.urls import path
from .views import chats_list_view, chat_view

app_name = 'im'
urlpatterns = [
    path('', chats_list_view, name='chat-list'),
    path('chat/<int:pk>', chat_view, name='chat')
]