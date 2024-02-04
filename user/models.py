from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='user-media/', default='default-profile.jpg')
    # followed = models.ManyToManyField(CustomUser, related_name='followed')

    def __str__(self):
        return f"{self.username}"
