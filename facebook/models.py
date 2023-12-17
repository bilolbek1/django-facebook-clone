from django.db import models
from user.models import CustomUser



class Post(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField()
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(CustomUser, related_name='liked', blank=True)

    def __str__(self):
        return self.title




NOTIFICATION_CHOICES = (
    ('See', 'See'),
    ('Saw', 'Saw')
)



class Review(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_created=True)


    def __str__(self):
        return f"{self.text[10]}... by {self.user_id}"




LIKE_CHOICES = (
    ('Liked', 'Liked'),
    ('Like', 'Like')
)


class Like(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)
    notification_status = models.CharField(choices=NOTIFICATION_CHOICES, max_length=3, default='See')




FOLLOW_CHOICES = (
    ('Followed', 'Followed'),
    ('Follow', 'Follow')
)



class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    follower_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_user')
    value = models.CharField(choices=FOLLOW_CHOICES, default='Follow', max_length=10)
    added_time = models.DateTimeField(auto_now_add=True)
    notification_status = models.CharField(choices=NOTIFICATION_CHOICES, max_length=3, default='See')

















