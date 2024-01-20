from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import CreatePostForm, ReviewForm
from user.models import CustomUser
from .models import Follow, Post, Like, Review, Save, Profile
import random


#################### THIS VIEW IS FOR PROFILE PAGE ############################

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user.id)
        print(posts)
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, 'user-profile.html', context)




###################### THIS VIEW IS FOR HOME PAGE ##############################

class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        # random_posts = random.sample(posts, 1)
        context = {
            'posts': posts,
            # 'random_posts': random_posts,
        }
        return render(request, 'home.html', context)




###################### THIS VIEW IS FOR POST DETAIL PAGE ##############################

class PostDetailView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        review_form = ReviewForm()
        print(post.review_set)
        context = {
            'user': request.user,
            'post': post,
            'review_form': review_form
        }
        return render(request, 'posts/post-detail.html', context)




###################### THIS VIEW IS FOR POST REVIEW ##############################


class PostReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        post = Post.objects.get(id=id)
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            Review.objects.create(
                user_id=request.user,
                post_id=post,
                text=review_form.cleaned_data['text']
            )

            messages.success(request, 'You added review.')
            return redirect(reverse('post-detail', kwargs={'id': post.id}))

        else:
            context = {
                'review_form': review_form
            }
            return render(request, 'posts/post-detail.html', context)






###################### THIS VIEW IS FOR CREATE POST PAGE ##############################

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreatePostForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create-post.html', context)

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                user_id=request.user,
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image'],
                text=form.cleaned_data['text'],
            )
            messages.success(request, 'You successfully created post!')
            return redirect('user-profile')

        else:
            context = {
                'form': form
            }
            return render(request, 'posts/create-post.html', context)






###################### THIS VIEW IS FOR EDIT POST PAGE ##############################

class EditPostView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        edit_post_form = CreatePostForm(instance=post)
        context = {
            'edit_post_form': edit_post_form
        }
        return render(request, 'posts/edit-post.html', context)

    def post(self, request, id):
        post = Post.objects.get(id=id)
        edit_post_form = CreatePostForm(instance=post,
                                        data=request.POST,
                                        files=request.FILES)
        if edit_post_form.is_valid():
            edit_post_form.save()

            messages.success(request, 'You successfully edited the post.')
            return redirect(reverse('post-detail', kwargs={'id': post.id}))

        else:
            context = {
                'edit_post_form': edit_post_form
            }
            return render(request, 'posts/edit-post.html', context)





###################### THIS VIEW IS FOR DELETE POST PAGE ##############################

class DeletePostView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('user-profile')




###################### THIS VIEW IS FOR USERS LIST PAGE ##############################


class UsersListView(View):
    def get(self, request):
        users = CustomUser.objects.exclude(username=request.user.username)
        context = {
            'users': users
        }
        return render(request, 'user/users_list.html', context)




###################### THIS VIEW IS FOR USERS LIST PAGE ##############################

class UserDetailView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        posts = Post.objects.filter(user_id=user)
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, 'user/user_detail.html', context)










class NotificationView():
    pass





class FollowView(View):
    def get(self, request):
        request_user = request.user
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        user_profile = user.profile

        context = {
            'user': user,
            'user_profile': user_profile,
        }

        return render(request, 'user/user_detail.html', context)

    def post(self, request):
        request_user = request.user
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        user_profile = user.profile

        if request_user in user_profile.followed.all():
            user.profile.followed.remove(request_user)
        else:
            user.profile.followed.add(request_user)

        follow, created = Follow.objects.get_or_create(user=user, follower_user=request_user)

        if not created:
            if follow.value == 'Followed':
                follow.value = 'Follow'
            else:
                follow.value = 'Followed'
        follow.save()




        return redirect(reverse('user-detail', kwargs={'id': user.id}))



class PostLikeView(LoginRequiredMixin, View):
    def get(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = request.user
        print(post)
        context = {
            'post': post,
            'user': user,
        }
        return render(request, 'posts/post-detail.html', context)

    def post(self, request):
        post_id = request.POST.get('post_id')
        user = request.user
        post = Post.objects.get(id=post_id)
        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)

        like, created = Like.objects.get_or_create(user_id=user, post_id=post)

        if not created:
            if like.value == 'Liked':
                like.value = 'Like'
            else:
                like.value = 'Liked'
        like.save()



        return redirect('post-detail', id=post_id)




class PostSaveView(LoginRequiredMixin, View):
    def get(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = request.user
        context = {
            'post': post,
            'user': user,
        }
        return render(request, 'posts/post-detail.html', context)

    def post(self, request):
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        user = request.user

        if user not in post.saved.all():
            post.saved.add(user)
        else:
            post.saved.remove(user)


        saved, created = Save.objects.get_or_create(user_id=user, post_id=post)

        if not created:
            if saved.value == 'Saved':
                saved.value = 'Save'
            else:
                saved.value = 'Saved'
        saved.save()



        return redirect('post-detail', id=post_id)




class SavedPostPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(saved=user)
        context = {
            'posts': posts
        }
        return render(request, 'posts/saved-post.html', context)



class LikedPostPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(liked=user)
        context = {
            'posts': posts
        }
        return render(request, 'posts/liked-post.html', context)



class MyPostsPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user)
        context = {
            'posts': posts
        }
        return render(request, 'posts/my-posts.html', context)



class FriendsListPageView(View):
    def get(self, request):
        user = request.user
        friends = user.profile.followed.all()
        context = {
            'friends': friends
        }

        return render(request, 'user/friends.html', context)









































































