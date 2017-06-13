from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.conf import settings

class StaffRequiredMixin():
    """
    View mixin which requires that the authenticated user is a staff member
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)