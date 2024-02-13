from django.test import TestCase
from facebook.models import Post, Profile
from django.urls import reverse

from user.models import CustomUser


class FacebookTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='test', password='test')
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')
        Profile.objects.create(user=self.user)
    def test_home_page(self):

        Post.objects.create(user_id=self.user, title='test1', text='test1', image="media-files/post-media/crismum.jpg")
        Post.objects.create(user_id=self.user, title='test2', text='test2', image="media-files/post-media/crismum.jpg")
        posts = Post.objects.all()

        response = self.client.get(reverse('home'))

        for i in posts:
            self.assertContains(response, i.text)
            self.assertContains(response, i.title)
            self.assertContains(response, i.image)


    def test_post_detail(self):

        post = Post.objects.create(user_id=self.user, title='test1', text='test1', image="media-files/post-media/crismum.jpg")

        response = self.client.get(reverse('post-detail', kwargs={'id': post.id}))

        self.assertContains(response, post.title)