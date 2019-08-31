from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.core.paginator import Paginator
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
    

def chat_view(request, pk):
    return HttpResponse('{}\'th chat placeholder'.format(pk))
