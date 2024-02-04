from django.forms import ModelForm
from django import forms

from chat.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']

    text = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'placeholder': 'Write message',
        'id': 'MessageInput'
    }))