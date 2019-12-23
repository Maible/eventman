from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from user.managers import UserManager


__all__ = ['User']


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

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('date_joined',)
