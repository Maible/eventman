from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden

from event.models import EventInvitation, AttendanceChoices

__all__ = ["AcceptInvitationView"]


class AcceptInvitationView(TemplateView):
    template_name = "web/invitation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invitation = get_object_or_404(EventInvitation, pk=self.kwargs.get('invitation_id'))
        if self.request.user.is_authenticated:
            if invitation.user != self.request.user:
                return Http404("You don't have access to this invitation!")
        elif not PasswordResetTokenGenerator().check_token(user=invitation.user, token=self.kwargs.get('token')):
            raise Http404("Token is not valid!")
        login(self.request, invitation.user)
        context['invitation'] = invitation
        context['current_view'] = "events"
        return context

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Login required!")
        invitation = get_object_or_404(EventInvitation, pk=self.kwargs.get('invitation_id'))
        accept_type = request.POST.get('accept_type')
        if accept_type == "accepted":
            invitation.attendance = AttendanceChoices.ATTENDING
        elif accept_type == "rejected":
            invitation.attendance = AttendanceChoices.NOT_ATTENDING
        elif accept_type == "partial":
            time_slot = request.POST.get('time_slot_id')
            invitation.attendance = AttendanceChoices.PARTIALLY_ATTENDING
            invitation.interval_id = int(time_slot)
        else:
            return HttpResponseForbidden("Unknown post data!")
        invitation.save()
        invitations = EventInvitation.objects.filter(user=request.user)[:20]
        return render(
            request, "web/invitation_completed.html", context={"invitations": invitations, "current_view": "events"}
        )

