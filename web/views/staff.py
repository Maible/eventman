"""
Views for staff members.
"""
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from web.mixins import StaffOnlyMixin
from event.models import Event, AttendanceChoices
from user.models import Contact


__all__ = ['EventsListView', 'EventInvitationsListView']


class EventsListView(StaffOnlyMixin, TemplateView):
    template_name = "web/staff/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('-created_at')[:50]
        context['contacts_count'] = Contact.objects.count()
        context['current_view'] = 'events'
        return context


class EventInvitationsListView(StaffOnlyMixin, TemplateView):
    template_name = "web/staff/invitations.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(Event, pk=kwargs.get('event_id'))
        context['event'] = event
        context['waiting'] = event.invitations.filter(attendance=AttendanceChoices.UNKNOWN)
        context['accepted'] = event.invitations.filter(
            Q(attendance=AttendanceChoices.ATTENDING) | Q(attendance=AttendanceChoices.PARTIALLY_ATTENDING)
        )
        context['declined'] = event.invitations.filter(attendance=AttendanceChoices.NOT_ATTENDING)
        return context
