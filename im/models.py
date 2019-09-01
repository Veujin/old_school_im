from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):

    users = models.ManyToManyField(User, through='ChatToUser')


    def __str__(self):
        return '; '.join([u.username for u in self.users.all()])


class ChatToUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    messages_unread = models.IntegerField(default=0)


class Message(models.Model):
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    sent_date = models.DateTimeField()


    def __str__(self):
        return '{}: {}'.format(self.owner, self.text[0:50])
