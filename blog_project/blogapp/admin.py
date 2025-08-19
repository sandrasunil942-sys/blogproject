from django.contrib import admin
from django.contrib import admin
from .models import Profile, BlogPost, Comment

# Register models
admin.site.register(Profile)
admin.site.register(BlogPost)
admin.site.register(Comment)

# Register your models here.
