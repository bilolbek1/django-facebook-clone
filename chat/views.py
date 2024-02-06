from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView

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
        for i in messages:
            if i.send_user != request.user and i.send_status == 'sending':
                i.send_status = 'sent'
                i.save()

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



class ContactListView(LoginRequiredMixin, View):
    def get(self, request):
        user = CustomUser.objects.get(username=request.user.username)
        contacts = user.profile.chats.all()
        search = request.GET.get('q', '')
        if search:
            contacts = contacts.filter(
                Q(first_name__icontains=search) | Q(username__icontains=search)
            )

        user_messages = {}
        for i in contacts:
            just = {}
            message = Message.objects.filter(
                Q(Q(send_user=user) & Q(recipient_user=i)) | Q(
                    Q(send_user=i) & Q(recipient_user=user))
            ).last()
            mes = Message.objects.filter(
                Q(Q(send_user=i) & Q(recipient_user=request.user)) | Q(
                    Q(send_user=request.user) & Q(recipient_user=i))
            )
            count = mes.filter(
                Q(send_status='sending') & Q(send_user=i) & Q(recipient_user=request.user)
            ).count()
            just[count] = message
            user_messages[i] = just

        print(user_messages)
        context = {
            "contacts": contacts,
            'user_messages': user_messages,
            'search': search,
        }
        return render(request, 'contacts.html', context)



class DeleteMessageView(LoginRequiredMixin, DeleteView):
    def post(self, request, username, id):
        user = CustomUser.objects.get(username=username)
        del_message = Message.objects.get(id=id, send_user=request.user, recipient_user=user)

        del_message.delete()
        messages.success(request, 'Message deleted')

        return redirect(reverse('user-chat', kwargs={'username': username}))















