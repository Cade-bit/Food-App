from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#--------------------> receiving a signal from a user to build their profile
@receiver(post_save, sender= User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)

#------------------------> Saving the user's profile
@receiver(post_save, sender= User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



