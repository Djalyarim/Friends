# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

# from posts.models import Profile_id, User



class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# @receiver(post_save, sender=User)
# def save_or_create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile_id.objects.create(user=instance)
#     else:
#         try:
#             instance.profile_id.save()
#         except ObjectDoesNotExist:
#             Profile_id.objects.create(user=instance)
