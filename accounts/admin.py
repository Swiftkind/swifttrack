from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Account, Payroll, AccountLog


class AccountLogAdmin(admin.ModelAdmin):
    list_display = ['account', 'status', 'date_created', 'ip']

    class Meta:
        model = AccountLog

admin.site.register(Account)
admin.site.register(Payroll)
admin.site.register(AccountLog, AccountLogAdmin)