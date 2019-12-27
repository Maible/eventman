from event.models import EventInvitation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@receiver(post_save, sender=EventInvitation)
def send_invitation_email(sender, instance, created, *args, **kwargs):
    if created:
        token = PasswordResetTokenGenerator().make_token(instance.user)
        event_id = instance.pk
        url = f"https://eventman.debugwith.me/accept/{event_id}/{token}/"
        send_mail(
            subject="You are invited to {event}".format(event=instance.event.title),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=instance.user.email_list,
            message=f"Please, accept invitation at {url}"
        )
