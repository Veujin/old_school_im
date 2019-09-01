from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Chat, Message, ChatToUser

class ChatsView(generic.ListView):

    context_object_name = 'chats_to_users'
    paginate_by = 20
    template_name = 'im/chat_list_view.html'


    def get_queryset(self):
        user = self.request.user
        return ChatToUser.objects.filter(user=user)

    
    def post(self, request, *args, **kwargs):
        try:
            new_user = User.objects.get(username=request.POST['username'])
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('im:chat-list'))

        users_only_chats = self.__get_users_only_chats(request.user, new_user)
        
        if users_only_chats:
            return HttpResponseRedirect(reverse(
                'im:chat', 
                args=(users_only_chats[0].id,)))
        
        if not users_only_chats:
            new_chat = Chat.objects.create()
            new_chat.users.add(new_user)
            new_chat.users.add(request.user)
            return HttpResponseRedirect(reverse(
                'im:chat', 
                args=(new_chat.id,)))

        return HttpResponseRedirect(reverse('im:chat-list'))

    
    def __get_users_only_chats(self, user1, user2):
        user1_chats = user1.chat_set.all()
        user2_chats = user2.chat_set.all()

        users_chats_intersection = user1_chats & user2_chats
        return [c for c in users_chats_intersection 
                            if set(c.users.all()) == set([user1, user2])]
    

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