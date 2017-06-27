from django.contrib import admin
from .models import Requests, Misc


class MiscAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'types', 'total_amount', 'months', 'date_created', 'status']
    list_filter = ('types', 'date_created',)

admin.site.register(Requests)
admin.site.register(Misc, MiscAdmin)
