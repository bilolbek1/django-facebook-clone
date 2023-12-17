from django.contrib import admin
from .models import Post, Like, Follow, Review


admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Review)
admin.site.register(Follow)