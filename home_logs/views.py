from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Tag, LogEntry

User = get_user_model()

def home(request):
    """Home page view"""
    return render(request, 'home_logs/index.html')


@login_required
def user_list(request):
    """List all users (for admin/moderation)"""
    users = User.objects.all().order_by('username')
    return render(request, 'home_logs/users/list.html', {'users': users})


@login_required
def user_detail(request, user_id):
    """Display individual user profile"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'home_logs/users/detail.html', {'user': user})


@login_required
def tag_list(request):
    """List all tags"""
    tags = Tag.objects.all().order_by('name')
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'home_logs/tags/list.html', {'tags': tags})
@login_required
def tag_detail(request, pk):
    """Display tag details and associated logs"""
    tag = get_object_or_404(Tag, pk=pk)
    return render(request, 'home_logs/tags/detail.html', {'tag': tag})


@login_required
def log_list(request):
    """List all logs, newest first"""
    logs = LogEntry.objects.all().order_by('-date')
   # logs = LogEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'home_logs/logs/list.html', {'logs': logs})

@login_required
def log_detail(request, log_id):
    """Display individual log entry"""
    log = get_object_or_404(LogEntry, id=log_id)
    return render(request, 'home_logs/logs/detail.html', {'log': log})