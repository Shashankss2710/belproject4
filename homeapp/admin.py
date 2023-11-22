from django.contrib import admin
from .models import LikePost, Post

admin.site.register(Post)
admin.site.register(LikePost)