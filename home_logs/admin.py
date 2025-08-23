from django.contrib import admin
from .models import Tag, LogEntry  # 🐍 REMOVED: User import

# 🐍 Inline logs inside Tag
class LogEntryInline(admin.TabularInline):
    model = LogEntry.tags.through  # ✅ The through table (M2M link)
    extra = 1
    verbose_name = "Related Log"
    verbose_name_plural = "Related Logs"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name", "user__username")
    inlines = [LogEntryInline]  # ✅ Add logs inline

# 🐍 LogEntry Admin  
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "content", "date", "mood")
    list_filter = ("date", "mood", "tags")
    search_fields = ("content", "user__username")
    filter_horizontal = ("tags",)  # ✅ Easy many-to-many picker