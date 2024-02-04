from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from user.models import CustomUser
from .forms import MessageForm
from .models import Message, Contact


class UserChatView(LoginRequiredMixin, View):
    def get(self, request, username):
        message_form = MessageForm()
        user = CustomUser.objects.get(username=username)
        print(user)
        messages = Message.objects.filter(
            Q(Q(send_user=user) & Q(recipient_user=request.user)) | Q(Q(send_user=request.user) & Q(recipient_user=user))
        )
        messages = messages.order_by('created_time')
        context = {
            'user': user,
            'messages': messages,
            'message_form': message_form,
        }
        return render(request, 'chat.html', context)



class MessageView(LoginRequiredMixin, View):
    def post(self, request, username):
        user = CustomUser.objects.get(username=username)
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            Message.objects.create(
                text=message_form.cleaned_data['text'],
                send_user=request.user,
                recipient_user=user
            )
            print(message_form.errors)

            return redirect(reverse('user-chat', kwargs={'username':username}))

        else:
            context = {
                'message_form': message_form,
            }
            return render(request, 'chat.html', context)



class ContactUncontacttView(LoginRequiredMixin, View):
    def get(self, request):
        request_user = CustomUser.objects.get(username=request.user.username)
        username = request.POST.get('user')
        user = CustomUser.objects.get(username=username)
        profile = request_user.profile

        context = {
            'user': user,
            'profile': profile,
            'request_user': request_user,
        }
        return render(request, 'chat.html', context)

    def post(self, request):
        request_user = CustomUser.objects.get(username=request.user.username)
        username = request.POST.get('user')
        user = CustomUser.objects.get(username=username)
        profile = request_user.profile

        if user in request_user.profile.chats.all():
            profile.chats.remove(user)
        else:
            profile.chats.add(user)

        contact, created = Contact.objects.get_or_create(user=user, request_user=request.user)

        if not created:
            if contact.value == 'Contacted':
                contact.value = 'Contact'
            else:
                contact.value = 'Contacted'
        contact.save()

        return redirect(reverse('user-chat', kwargs={'username': user.username}))



















