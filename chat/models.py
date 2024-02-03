from django.contrib.auth.models import User
from django.db import models

from user.models import CustomUser


MESSAGES_TYPE = (
    ('sent', 'sent'),
    ('sending', 'sending')
)


class Message(models.Model):
    send_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender', null=True)
    recipient_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipient', null=True)
    text = models.TextField()
    send_status = models.CharField(max_length=10, choices=MESSAGES_TYPE, default='sending')
    created_time = models.DateTimeField(auto_now_add=True)



