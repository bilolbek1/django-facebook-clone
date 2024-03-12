from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import CreatePostForm, ReviewForm
from user.models import CustomUser
from .models import Follow, Post, Like, Review, Save, Profile
import random


#################### USER PROFILE PAGE ############################

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user.id)
        followers_count = user.profile.followed.all().count()
        following_count = Profile.objects.filter(followed=user).count()
        print(posts)
        context = {
            'user': user,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
        }
        return render(request, 'user-profile.html', context)




###################### HOME PAGE ##############################

class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.all()
        if posts.count() < 20:
            count = posts.count()
            posts = random.sample(list(posts), count)
        else:
            posts = random.sample(list(posts), 20)
        user = CustomUser.objects.get(id=request.user.id)
        contacts = user.profile.chats.all()
        context = {
            'posts': posts,
            'contacts': contacts,
        }
        return render(request, 'home.html', context)




###################### POST DETAIL PAGE ##############################

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




###################### POST'S REVIEW ##############################


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






###################### CREATE POST PAGE ##############################

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






###################### EDIT POST PAGE ##############################

class EditPostView(LoginRequiredMixin, View):
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





###################### DELETE POST PAGE ##############################

class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, id):
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('user-profile')





###################### USERS DETAIL PAGE ##############################

class UserDetailView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        posts = Post.objects.filter(user_id=user)
        followings = Profile.objects.filter(followed=user).count()
        context = {
            'user': user,
            'posts': posts,
            'followings': followings,
        }
        return render(request, 'user/user_detail.html', context)










class NotificationView():
    pass




###################### FOLLOW SYSTEM ##############################

class FollowView(LoginRequiredMixin, View):
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





###################### POST LIKE SYSTEM ##############################

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






###################### POST SAVE SYSTEM ##############################

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





###################### USER'S SAVED POSTS ##############################

class SavedPostPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(saved=user)
        posts = posts.order_by('-id')
        context = {
            'posts': posts
        }
        return render(request, 'posts/saved-post.html', context)






###################### USER'S LIKED POSTS ##############################

class LikedPostPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(liked=user)
        posts = posts.order_by('-id')
        context = {
            'posts': posts
        }
        return render(request, 'posts/liked-post.html', context)







###################### MY CREATED POSTS ##############################

class MyPostsPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user)
        posts = posts.order_by('-id')
        context = {
            'posts': posts
        }
        return render(request, 'posts/my-posts.html', context)






###################### FRIENDS LIST ##############################

class FriendsListPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        friends = user.profile.followed.all()
        friends_2 = []
        profiles = Profile.objects.filter(followed=user)
        for i in profiles:
            if i.user in friends:
                continue
            else:
                friends_2.append(i.user)
        print(friends_2)
        print(friends)
        context = {
            'friends': friends,
            'friends_2': friends_2,
        }

        return render(request, 'user/friends.html', context)




###################### REQUEST USER'S FOLLOWERS PAGE ##############################

class UserFollowersPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        search = request.GET.get('q', '')
        followers = user.profile.followed.all()
        if search:
            followers = followers.filter(
                Q(username__icontains=search)
            )
        context = {
            'followers': followers,
            'search': search,
        }
        return render(request, 'user/followers.html', context)




###################### REQUEST USER'S FOLLOWING PAGE ##############################

class UserFollowingsPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        search = request.GET.get('q', '')
        profiles = Profile.objects.filter(followed=user)
        if search:
            profiles = profiles.filter(
                Q(user__username__icontains=search)
            )
        followings = []
        for i in profiles:
            followings.append(i.user)

        context = {
            'followings': followings,
            'search': search,
        }
        return render(request, 'user/following.html', context)





###################### ALL USERS SEARCH ##############################

class SearchUsersPageView(View):
    def get(self, request):
        search = request.GET.get('q', '')
        users = CustomUser.objects.exclude(username=request.user.username)
        if search:
            users = users.filter(
                Q(username__icontains=search) | Q(first_name__icontains=search)
            )
        context = {
            'search': search,
            'users': users,
        }
        return render(request, 'user/users-search.html', context)





###################### DELETE REVIEW ##############################

def delete_review(request, post_id, review_id):
    post = get_object_or_404(Post, id=post_id)
    review = get_object_or_404(Review, id=review_id, post_id=post)

    if request.method == 'POST':
        review.delete()
        return redirect('post-detail', id=post.id)
    return render(request, 'posts/post-detail.html', {'review': review})





###################### USER'S FLLOWERS PAGE ##############################

class OneUserFollowersPageView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        search = request.GET.get('q', '')
        followers = user.profile.followed.all()
        if search:
            followers = followers.filter(
                Q(username__icontains=search)
            )
        context = {
            'followers': followers,
            'search': search,
        }
        return render(request, 'user/one-user-followers.html', context)




###################### USER'S FOLLOWING PAGE ##############################

class OneUserFollowingsPageView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        search = request.GET.get('q', '')
        profiles = Profile.objects.filter(followed=user)
        if search:
            profiles = profiles.filter(
                Q(user__username__icontains=search)
            )
        followings = []
        for i in profiles:
            followings.append(i.user)

        context = {
            'followings': followings,
            'search': search,
        }
        return render(request, 'user/one-user-following.html', context)
