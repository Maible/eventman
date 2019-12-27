from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User, Contact


@receiver(post_save, sender=User)
def make_default_contact(sender, instance, created, *args, **kwargs):
    if created:
        Contact.objects.create(
            user=instance, name=instance.get_full_name(), email=instance.email
        )
