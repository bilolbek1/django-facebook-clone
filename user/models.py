from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    image = models.ImageField()
    # followed = models.ManyToManyField(CustomUser, related_name='followed')
