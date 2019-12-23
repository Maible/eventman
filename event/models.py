from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import Q
from user.models import User


class AttendanceChoices(models.IntegerChoices):
    UNKNOWN = 0, _("Unknown")
    ATTENDING = 1, _("Accepted")
    PARTIALLY_ATTENDING = 2, _("Partially attending")
    NOT_ATTENDING = 3, _("Declined")


class Venue(models.Model):
    name = models.CharField(_("Name"), max_length=150, null=False, blank=False)
    address_first = models.CharField(_("Address 1"), max_length=255, null=True, blank=True)
    address_second = models.CharField(_("Address 2"), max_length=100, null=False, blank=False)
    max_capacity = models.IntegerField(_("Maximum capacity"), default=10)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Venue")
        verbose_name_plural = _("Venues")
        ordering = ('name',)


class Event(models.Model):
    title = models.CharField(_("Title"), max_length=150, null=False, blank=False)
    description = models.CharField(_("Short description"), max_length=255, null=True, blank=True)
    long_description = models.TextField(_("Long description"), null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, related_name='events', null=True, blank=True)
    capacity = models.IntegerField(_("Capacity"), default=10)
    guest_per_person = models.IntegerField(_("Allowed guests"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    @property
    def total_attending(self) -> int:
        total = 0
        invitations = self.invitations.filter(
            Q(attendance=AttendanceChoices.ATTENDING) | Q(attendance=AttendanceChoices.PARTIALLY_ATTENDING)
        )
        for invitation in invitations:
            total += 1
            total += invitation.guests.count()
        return total

    @property
    def start_time(self):
        return self.intervals.order_by('starts_at').first()

    @property
    def end_time(self):
        return self.intervals.order_by('ends_at').first()

    @property
    def invitations_count(self) -> int:
        return self.invitations.count()

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ('-created_at',)


class EventInterval(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='intervals')
    starts_at = models.DateTimeField(_("Start time"))
    ends_at = models.DateTimeField(_("End time"))
    description = models.CharField(_("Description"), max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return "{event} from {start} to {end}".format(
            event=self.event.title, start=self.starts_at, end=self.ends_at
        )

    class Meta:
        verbose_name = _("Event interval")
        verbose_name_plural = _("Event intervals")
        ordering = ('event', 'starts_at')


class EventInvitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='invitations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    interval = models.ForeignKey(EventInterval, on_delete=models.SET_NULL, null=True, blank=True)
    attendance = models.IntegerField(
        _("Attendance"), choices=AttendanceChoices.choices, default=AttendanceChoices.UNKNOWN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "{event} invitation for {user}".format(
            event=self.event.title, user=self.user
        )

    class Meta:
        verbose_name = _("Event invitation")
        verbose_name_plural = _("Event invitations")
        ordering = ('event', 'user')
        constraints = [models.UniqueConstraint(fields=['event', 'user'], name='unique_invitation')]


class EventGuest(models.Model):
    invitation = models.ForeignKey(EventInvitation, on_delete=models.CASCADE, related_name='guests')
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email address"), null=True, blank=True)
    phone = models.CharField(_("Phone number"), max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self) -> str:
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("Event guest")
        verbose_name_plural = _("Event guests")
        ordering = ('invitation', 'created_at')
