from django.db import models
from user.models import CustomUser




class Post(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post-media/')
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(CustomUser, related_name='liked', blank=True, null=True)
    saved = models.ManyToManyField(CustomUser, related_name='saved', blank=True, null=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.text}... by {self.user_id}"




LIKE_CHOICES = (
    ('Liked', 'Liked'),
    ('Like', 'Like')
)


Save_CHOICES = (
    ('Saved', 'Saved'),
    ('Save', 'Save')
)






class Like(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)




FOLLOW_CHOICES = (
    ('Followed', 'Followed'),
    ('Follow', 'Follow')
)



class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    follower_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_user')
    value = models.CharField(choices=FOLLOW_CHOICES, default='Follow', max_length=10)
    added_time = models.DateTimeField(auto_now_add=True)




class Save(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.CharField(choices=LIKE_CHOICES, default='Save', max_length=10)


    def __str__(self):
        return f"'{self.user_id.username}' for '{self.post_id.title}'"






class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    followed = models.ManyToManyField(CustomUser, related_name='following', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'












