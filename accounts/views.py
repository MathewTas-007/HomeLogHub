import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserChangeForm
from django.utils import timezone
from home_logs.models import LogEntry

from .forms import RegisterForm, LoginForm, ProfileForm

# ------------------------
# Custom forms
# ------------------------
class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

# ------------------------
# Profile view (single-page view/edit)
# ------------------------
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['form'] = ProfileForm(instance=user)
        context['user_logs_count'] = user.logentry_set.count()
        context['user_comments_count'] = 0  # placeholder
        context['user_likes_count'] = 0     # placeholder

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            print("✅ Profile updated successfully")
            return redirect('accounts:profile')
        else:
            print("❌ Profile form errors:", form.errors)
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

# ------------------------
# Password change
# ------------------------
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

# ------------------------
# Registration & login
# ------------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()

            # First log entry
            LogEntry.objects.create(
                user=user,
                date=timezone.now().date(),
                mood='😊',
                content="Welcome to your new journal! This is your first log."
            )

            send_verification_email(user, request)
            return redirect('accounts:verification_sent')
        else:
            print("❌ Registration form errors:", form.errors)
    else:
        form = RegisterForm()
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
                print(f"❌ Login failed for: {username}")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home_logs:home')

# ------------------------
# Email verification
# ------------------------
def send_verification_email(user, request):
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
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return render(request, 'accounts/verification_success.html')
        else:
            return render(request, 'accounts/verification_failed.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, 'accounts/verification_failed.html')
