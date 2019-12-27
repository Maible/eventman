from django.contrib import admin
from django.conf import settings as django_settings
from django.conf.urls.static import static
from django.urls import path
from web.views import staff, events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/events/', staff.EventsListView.as_view(), name='staff_events_list'),
    path('staff/events/<int:event_id>/', staff.EventInvitationsListView.as_view(), name='staff_event_invitations'),
    path('accept/<int:invitation_id>/<token>/', events.AcceptInvitationView.as_view(), name='accept_event_invitation'),
]

if django_settings.DEBUG:
    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)
    urlpatterns += static(django_settings.STATIC_URL, document_root=django_settings.STATIC_ROOT)
