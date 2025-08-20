"""Defines URL patterns for home_logs."""
from django.urls import path
from . import views

app_name = 'home_logs'
urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.user_list, name='user_list'), # List all users
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    # Tags
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
    
    # Logs
    path('logs/', views.log_list, name='log_list'),
    path('logs/<int:log_id>/', views.log_detail, name='log_detail'),

]