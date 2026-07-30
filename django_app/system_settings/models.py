from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    THEME_CHOICES = [
        ('light', 'Light Medical Theme'),
        ('dark', 'Dark Cyber-Medical Theme'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English (US)'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    email_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Settings"
