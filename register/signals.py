from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Foydalanuvchi, Profile

@receiver(post_save, sender=Foydalanuvchi)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
