from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Chat, Message


def chats_list_view(request):
    page = request.GET.get('page', 1)
    
    user = request.user
    user_chats = user.chat_set.all()
    paginator = Paginator(user_chats, 25)
    chats_page = paginator.get_page(page)

    for c in chats_page:
        chat_usernames = [u.username for u in c.users.all()]
        chat_name = ', '.join([u for u in chat_usernames if u != user.username])

        # last_chat_message = c.message_set.all().latest('sent_date')

        c.chat_name = chat_name
        # c.last_message = last_chat_message


    context = {'chats_page': chats_page}
    return render(request, 'im/chat_list_view.html', context=context)
    

class ChatMessagesView(generic.ListView):

    context_object_name = 'messages'
    paginate_by = 20
    template_name = 'im/chat_messages_view.html'
    model = Message


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