from django.urls import path
from . import views

app_name = 'im'
urlpatterns = [
    path('', views.chats_list_view, name='chat-list'),
    path('chat/<int:chat_id>', views.ChatView.as_view(), name='chat')
]