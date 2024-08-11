# forum/urls.py

from django.urls import path
from .views import CategoryListCreateView, ThreadListCreateView, PostListCreateView, CommentListCreateView, AnnouncementListView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('threads/', ThreadListCreateView.as_view(), name='thread-list-create'),
    path('threads/<int:thread_id>/posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
]
