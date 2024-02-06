from django.urls import path
from .views import UserChatView, MessageView, ContactUncontacttView, ContactListView, \
DeleteMessageView


urlpatterns = [
    path('<str:username>/', UserChatView.as_view(), name='user-chat'),
    path('<str:username>/message', MessageView.as_view(), name='message'),
    path('contact', ContactUncontacttView.as_view(), name='contact'),
    path('contact/list', ContactListView.as_view(), name='contact-list'),
    path('<str:username>/user/<int:id>/message/delete', DeleteMessageView.as_view(), name='message-delete'),
]