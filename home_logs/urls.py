"""Defines URL patterns for home_logs."""
from django.urls import path
from . import views

app_name = "home_logs"  # 🐍 namespace for app URLs

urlpatterns = [
    path("", views.home, name="home"),  # 🐍 home page
    
    # Users
    path("users/", views.user_list, name="user_list"),  # 🐍 list all users
    path("users/<int:pk>/", views.user_detail, name="user_detail"),  # 🐍 user detail by primary key
    
    # Tags  
    path("tags/", views.tag_list, name="tag_list"),  # 🐍 list all tags
    path("tags/<int:pk>/", views.tag_detail, name="tag_detail"),  # 🐍 tag detail by primary key
    
    # Logs
    path("logs/", views.log_list, name="log_list"),  # 🐍 list logs for logged-in user
    path("logs/<int:pk>/", views.log_detail, name="log_detail"),  # 🐍 log detail by primary key
]