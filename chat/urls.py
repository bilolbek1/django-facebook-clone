from django.urls import path
from .views import UserChatView, MessageView, ContactUncontacttView


urlpatterns = [
    path('<str:username>/', UserChatView.as_view(), name='user-chat'),
    path('<str:username>/message', MessageView.as_view(), name='message'),
    path('contact', ContactUncontacttView.as_view(), name='contact'),
]