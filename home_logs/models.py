from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.conf import settings # Best pratice for User reference
from django.utils import timezone # add this line

# Create your models here. 


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    date_format = models.CharField(max_length=20, default='YYYY-MM-DD')
    
    # Add these lines to prevent clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='home_logs_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='home_logs_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # References your custom User.
        on_delete=models.CASCADE,
        related_name='tags'
    )

    class Meta:
        unique_together = ('name', 'user') # Prevent duplicate tags per user.

    def __str__(self):
        return f"{self.user.username}'s tag: {self.name}"

class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, related_name="logs")

    def __str__(self):
        return f"{self.user.username}'s log: {self.date}"
