from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # posts
    path('new-post/', views.CreatePostView.as_view(), name='new_post'),
    path('<slug>/<pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('like-post/', views.post_like, name='post_like'),
    path('update/post/<pk>/', views.UpdateBlogPostView.as_view(), name='update_post'),
    path('delete/post/<pk>', views.DeleteBlogPostView.as_view(), name='delete_post'),
    path('delete/comment/<pk>', views.CommentDelete.as_view(), name='delete_comment'),

    # topics
    path('all-topics/', views.AllTopicView.as_view(), name='all_topics'),
    path('topic/posts/<id>/', views.topic_posts, name='topic_posts'),

    # tags
    path('tag-posts/<tag_slug>', views.tag_post, name='tag_posts'),
]
