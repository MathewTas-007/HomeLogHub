from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

from .forms import SignUpForm, LoginForm, ProfileForm

# ================================
# CUSTOM USER FORM CLASSES
# ================================
class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove the password field
    
    class Meta:
        model = get_user_model()  # Use your custom user model
        fields = ('username', 'email', 'first_name', 'last_name')

# ================================
# CLASS-BASED VIEWS
# ================================
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

# ================================
# AUTH VIEWS
# ================================
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False  # New users start unverified
            user.save()
            send_verification_email(user, request)
            return redirect('accounts:verification_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_logs:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home_logs:home')

# ================================
# PROFILE VIEW
# ================================
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

# ================================
# EMAIL VERIFICATION VIEWS
# ================================
def send_verification_email(user, request):
    """Send email verification link to user."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    subject = "Verify Your Email"
    message = render_to_string('accounts/verify_email.html', {
        'user': user,
        'uid': uid,
        'token': token,
    })
    send_mail(subject, message, None, [user.email])

@login_required
def verify_email(request, uidb64, token):
    User = get_user_model()  # Get your custom user model
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):  # Fixed typo: 'use' -> 'user'
            user.email_verified = True
            user.save()
            return render(request, 'accounts/verification_success.html')
        else:
            return render(request, 'accounts/verification_failed.html')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):  # Fixed typo: 'DoesNotError' -> 'DoesNotExist'
        return render(request, 'accounts/verification_failed.html')

# ================================
# 🧼 SIGNUP BACTERIA REMOVED:
# ================================
# ❌ DELETED: def signup(request): 
# ❌ DELETED: UserCreationForm imports and usage
# ❌ DELETED: Redundant django.contrib.auth.models.User import