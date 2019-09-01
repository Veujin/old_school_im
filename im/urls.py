from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'im'
urlpatterns = [
    path('chats', login_required(views.ChatsView.as_view()), name='chat-list'),
    path('chats/<int:chat_id>', login_required(views.ChatMessagesView.as_view()), name='chat')
]