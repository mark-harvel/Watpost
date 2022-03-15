from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [
    path('profile/<username>/<pk>/', views.MyProfileView.as_view(), name='profile'),
    path('account/<username>/<pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('edit-profile/<pk>/', views.EditProfile.as_view(), name='edit_profile'),
    path('follow/', views.user_follow, name='user_follow'),
    path('subs/', views.SubsView.as_view(), name='subs'),
]
