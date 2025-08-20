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
from django.contrib.auth.models import User


from .forms import SignUpForm, LoginForm, ProfileForm  # Make sure these exist in forms.py


# form for editing user profile (excluding password)
class CustomUserChangeForm(UserChangeForm):
    password = None #  Remove the password field
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',  'last_name')

# View to display the user's profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

# View to edit the user's profile
class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

#  View to change password 
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change'
    success_url = reverse_lazy('accounts:profile')
# ================================
# AUTH VIEWS
# ================================
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # added later
            user.email_verified = False # New users start unverified
            user.save()
            # 🚀 Send verification email after registration
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
def send_verification_email(request, user):
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
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(use, token):
            user.email_verified = True # Add this field to your User model
            user.save()
            return render(request, 'accounts/verification_success.html')
        else:
            return render(request, 'accounts/verification_failed.html')

    except (TypeError, ValueError, OverflowError, User.DoesNotError):
        return render(request, 'accounts/verification_failed.html')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  # Redirect to login after success
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})