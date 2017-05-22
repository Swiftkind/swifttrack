from accounts.mixins import AccountTimestamp

class TimestampMiddleware(AccountTimestamp):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        # check if there is a logged in user
        if request.user.is_authenticated() and not request.user.is_superuser:
            self.record(request)

        return response