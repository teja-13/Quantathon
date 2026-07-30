from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, default='+1 (555) 019-2834')
    title = models.CharField(max_length=100, default='Senior Oncologist')
    department = models.CharField(max_length=100, default='Diagnostic Oncology & Radiology')
    bio = models.TextField(blank=True, default='Board-certified oncologist specializing in early-stage detection and AI-assisted clinical workflow integration.')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
