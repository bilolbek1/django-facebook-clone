from django.shortcuts import render
from django.views import View

from user.models import CustomUser
from .models import Follow, Post, Like, Review


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html', context)




class PostDetailView(View):
    pass





class CreatePostView(View):
    pass




class EditPostView(View):
    pass




class DeletePostView(View):
    pass




class NotificationView():
    pass





class FollowView(View):
    pass




















































































