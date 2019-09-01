from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Chat, Message

class ChatsView(generic.ListView):

    context_object_name = 'chats'
    paginate_by = 20
    template_name = 'im/chat_list_view.html'

    def get_queryset(self):
        user = self.request.user
        return user.chat_set.all()
    

class ChatMessagesView(generic.ListView):

    context_object_name = 'messages'
    paginate_by = 20
    template_name = 'im/chat_messages_view.html'


    def get_queryset(self):
        chat = get_object_or_404(Chat, pk=self.kwargs['chat_id'])
        return Message.objects.filter(chat=chat)


    def get_context_data(self, **kwargs):
        chat = get_object_or_404(Chat, pk=self.kwargs['chat_id'])
        companions = [u for u in chat.users.all() 
                      if u.username != self.request.user.username]
        
        context = super().get_context_data(**kwargs)
        context['chat'] = chat
        context['companions'] = companions
        return context


    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs['chat_id'])
        user = request.user
        message = request.POST['message']

        chat.message_set.create(owner=user, text=message, sent_date=timezone.now())

        return HttpResponseRedirect(reverse('im:chat', args=(kwargs['chat_id'],)))