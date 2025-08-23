from django.utils import timezone # added later
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from .models import Tag, LogEntry


User = get_user_model()

def home(request):
    return render(request, 'home_logs/index.html')

@login_required
def user_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Staff access required.")
    users = User.objects.all().order_by('username')
    return render(request, 'home_logs/users/list.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, id=pk)
    if request.user != user and not request.user.is_staff:
        return HttpResponseForbidden("Cannot view other users' profiles.")
    return render(request, 'home_logs/users/detail.html', {'user': user})

@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'home_logs/tags/list.html', {'tags': tags})

@login_required
def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if tag.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Cannot view other users' tags.")
    return render(request, 'home_logs/tags/detail.html', {'tag': tag})

@login_required
def log_list(request):
    logs = LogEntry.objects.filter(user=request.user).order_by('-date')

    for log in logs:
        if not log.date:
            log.date = timezone.now().date()
        if not log.mood:
            log.mood = '😐'

    return render(request, 'home_logs/logs/list.html', {'logs': logs})

@login_required
def log_detail(request, pk):
    # 🐍 CLEANED: Removed redundant permission check
    log = get_object_or_404(LogEntry, id=pk, user=request.user)
    return render(request, 'home_logs/logs/detail.html', {'log': log})