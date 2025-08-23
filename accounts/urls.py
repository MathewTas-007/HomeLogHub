"""URL patterns for accounts app."""
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "accounts"

urlpatterns = [
    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    
    # Profile (single-page view & edit)
    
    # Password change
    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),

    # Redirects for legacy routes
    path("signup/", RedirectView.as_view(
        pattern_name="accounts:register", 
        permanent=True
    ), name="signup_legacy"),

    # Redirect root of accounts/ to profile (default for auth)
    path("", RedirectView.as_view(
        pattern_name="accounts:profile", 
        permanent=False
    ), name="account_root"),
]
