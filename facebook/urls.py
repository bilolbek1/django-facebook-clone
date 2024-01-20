from django.urls import path
from .views import HomePageView, PostDetailView, EditPostView, CreatePostView, DeletePostView, \
ProfileView, PostReviewView, UsersListView, UserDetailView, FollowView, PostLikeView, PostSaveView, \
SavedPostPageView, LikedPostPageView, MyPostsPageView, FriendsListPageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<int:id>/', PostDetailView.as_view(), name='post-detail'),
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('edit-post/<int:id>/', EditPostView.as_view(), name='edit-post'),
    path('delete-post/<int:id>/', DeletePostView.as_view(), name='delete-post'),
    path('user-profile/', ProfileView.as_view(), name='user-profile'),
    path('post/<int:id>/review/', PostReviewView.as_view(), name='post-review'),
    path('user/list/', UsersListView.as_view(), name='user-list'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('user/follow', FollowView.as_view(), name='follow'),
    path('post/like', PostLikeView.as_view(), name='post-like'),
    path('post/save', PostSaveView.as_view(), name='post-save'),
    path('user/saved/', SavedPostPageView.as_view(), name='user-saved'),
    path('user/liked/', LikedPostPageView.as_view(), name='user-liked'),
    path('my/posts/', MyPostsPageView.as_view(), name='my-posts'),
    path('user/friends/', FriendsListPageView.as_view(), name='user-friends'),


]