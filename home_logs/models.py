
from django.db import models
from django.conf import settings
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags'
    )

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']

    def __str__(self):
        return f"#{self.name}"

class LogEntry(models.Model):
    MOOD_CHOICES = [
        ('😊', 'Happy'),
        ('😐', 'Neutral'),
        ('😢', 'Sad'),
        ('🔥', 'Energetic'),
        ('😴', 'Tired'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    date = models.DateField(default=timezone.now)
    content = models.TextField()
    mood = models.CharField(
        max_length=2,
        choices=MOOD_CHOICES,
        blank=True,
        null=True
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='logs',
        blank=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Log Entries'

    def __str__(self):
        return f"{self.user.username}'s log on {self.date}"
