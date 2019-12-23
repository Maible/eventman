from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from user.managers import UserManager


__all__ = ['User', 'Contact']


class User(AbstractUser):
    email = models.EmailField(
        _('Email'), unique=True, blank=False, null=False,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return full_name
        if self.email:
            return self.email
        return self.username

    @property
    def created_at(self):
        return self.date_joined

    def phone_list(self):
        return self.contacts.filter(phone__isnull=False).values_list('phone', flat=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('date_joined',)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_("Email"), null=True, blank=True)
    phone = models.CharField(_("Phone number"), max_length=20, null=True, blank=True)
    has_telegram = models.BooleanField(_("Used for Telegram"), default=False)
    has_whatsapp = models.BooleanField(_("Used for Whatsapp"), default=False)
    address = models.TextField(_("Address"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        ordering = ('user', '-updated_at',)
