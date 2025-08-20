
from django.contrib.auth.models import AbstractUser
from django.db import models

# create your models here.

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    date_format = models.CharField(max_length=20, default='YYYY-MM-DD')