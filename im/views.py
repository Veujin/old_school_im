from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Chat


def chats_list_view(request):
    page = request.GET.get('page', 1)
    
    user = request.user
    user_chats = user.chat_set.all()
    paginator = Paginator(user_chats, 25)
    chats_page = paginator.get_page(page)

    for c in chats_page:
        chat_usernames = [u.username for u in c.users.all()]
        chat_name = ', '.join([u for u in chat_usernames if u != user.username])

        last_chat_message = c.message_set.all().latest('sent_date')

        c.chat_name = chat_name
        c.last_message = last_chat_message


    context = {'chats_page': chats_page}
    return render(request, 'im/chat_list_view.html', context=context)
    

class ChatView(generic.ListView):
    
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page',1)

        chat = get_object_or_404(Chat, pk=kwargs['chat_id'])
        user = request.user

        messages = chat.message_set.all().order_by('-sent_date')
        paginator = Paginator(messages, 25)
        messages_page = paginator.get_page(page)

        context = { 
            'messages_page': messages_page,
            'companions': [u for u in chat.users.all() if u.username != user.username],
            'chat': chat
        }
        return render(request, 'im/chat_view.html', context=context)
    
    
    def post(self, request, *args, **kwargs):
        chat = get_object_or_404(Chat, pk=kwargs['chat_id'])
        user = request.user
        message = request.POST['message']

        chat.message_set.create(owner=user, text=message, sent_date=timezone.now())

        return HttpResponseRedirect(reverse('im:chat', args=(kwargs['chat_id'],)))