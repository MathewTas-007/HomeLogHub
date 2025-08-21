# accounts/urls.py
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views
from .views import verify_email

app_name = 'accounts'

urlpatterns = [
    # 🔥 REDIRECT: Old URLs -> New register page
    path('signup/', RedirectView.as_view(
        url=reverse_lazy('accounts:register'), 
        permanent=True
    ), name='signup_legacy'),
    
    # ✅ ACTIVE AUTH ENDPOINTS
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # ✅ PROFILE MANAGEMENT
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    
    # ✅ PASSWORD RESET FLOW
    path('password-reset/', auth_views.PasswordResetView.as_view(  
        template_name='accounts/password_reset.html',  
        email_template_name='accounts/password_reset_email.html',  
        success_url=reverse_lazy('accounts:password_reset_done')  
    ), name='password_reset'),  
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(  
        template_name='accounts/password_reset_done.html'  
    ), name='password_reset_done'),  
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(  
        template_name='accounts/password_reset_confirm.html',  
        success_url=reverse_lazy('accounts:password_reset_complete')  
    ), name='password_reset_confirm'),  
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(  
        template_name='accounts/password_reset_complete.html'  
    ), name='password_reset_complete'),  
    
    # ✅ EMAIL VERIFICATION
    path('verify_email/<uidb64>/<token>/', verify_email, name='verify_email'),
]