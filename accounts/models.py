
from django.contrib.auth.models import AbstractUser
from django.db import models

# create your models here.

class User(AbstractUser):  # ✅ ONLY PLACE User SHOULD EXIST
    bio = models.TextField(blank=True, null=True)
    date_format = models.CharField(max_length=20, default='YYYY-MM-DD')
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users',  # 🐍 UNIQUE related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='accounts_users',  # 🐍 UNIQUE related_name
        blank=True,
    )