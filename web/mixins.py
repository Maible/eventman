from django.contrib.auth.mixins import AccessMixin


class StaffOnlyMixin(AccessMixin):
    """Allow only staff user to access the view."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
