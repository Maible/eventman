from django.contrib import admin
from event.models import Venue, Event, EventInterval, EventInvitation, EventGuest


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_capacity')
    search_fields = ('name',)


class InlineEventIntervalAdmin(admin.TabularInline):
    model = EventInterval


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'venue', 'guest_per_person', 'capacity', 'invitations_count', 'total_attending', 'created_at'
    )
    readonly_fields = ('created_at',)
    search_fields = ('title',)
    autocomplete_fields = ('venue',)
    inlines = [InlineEventIntervalAdmin]


@admin.register(EventInterval)
class EventIntervalAdmin(admin.ModelAdmin):
    list_display = ('event', 'starts_at', 'ends_at')
    search_fields = ('event__title', 'description')
    autocomplete_fields = ('event',)


@admin.register(EventInvitation)
class EventInvitationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'attendance', 'interval', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('event__title', 'user__email')
    autocomplete_fields = ('event', 'user', 'interval')


@admin.register(EventGuest)
class EventGuestAdmin(admin.ModelAdmin):
    list_display = ('invitation', 'full_name', 'email', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('first_name', 'last_name')
    autocomplete_fields = ('invitation',)
