from django.utils import timezone
from .models import AccountLog


class AccountTimestamp(object):

    def __init__(self, *args, **kwargs):
        return super(AccountTimestamp, self).__init__(*args, **kwargs)

    def get_client_ip(self, request):
        """ get the ip address based on the request
        """
        xforward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if xforward_for:
            return xforward_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def record(self, request):
        """ log item
        """
        if not self.has_record(request):
            AccountLog.objects.create(
                account=request.user,
                ip=self.get_client_ip(request),
            )

    def has_record(self, request):
        now = timezone.now()

        if AccountLog.objects.filter(
            account=request.user,
            date_created__date=now.date()).exists():
            return True
        return False