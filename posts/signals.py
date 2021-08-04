from django.contrib.auth.models import User
from django.db.models.signals import post_save


def save_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(save_profile, sender=User)
