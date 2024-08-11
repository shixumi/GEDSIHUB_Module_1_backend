# forum/admin.py

from django.contrib import admin
from .models import Category, Thread, Post, Comment, Announcement

admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Announcement)
