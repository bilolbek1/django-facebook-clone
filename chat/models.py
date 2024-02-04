from django.contrib.auth.models import User
from django.db import models

from user.models import CustomUser


MESSAGES_TYPE = (
    ('sent', 'sent'),
    ('sending', 'sending')
)


CONTACT_CHOICES = (
    ('Contacted', 'Contacted'),
    ('Contact', 'Contact')
)



class Message(models.Model):
    send_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True)
    recipient_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient', null=True)
    text = models.TextField()
    send_status = models.CharField(max_length=10, choices=MESSAGES_TYPE, default='sending')
    created_time = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_user', null=True)
    request_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='request_user', null=True)
    value = models.CharField(choices=CONTACT_CHOICES, default='Contact', max_length=10)
    added_time = models.DateTimeField(auto_now_add=True)

