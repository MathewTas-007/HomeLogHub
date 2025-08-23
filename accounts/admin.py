from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "date_joined", "is_staff")
    search_fields = ("username", "email")
    # Add custom fields to admin form
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("bio", "date_format")}),
    )