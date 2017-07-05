from django import template
from django.utils import timezone
from datetime import datetime, timedelta

from accounts.models import Account
from projects.models import Project

register = template.Library()

@register.assignment_tag
def all_employees():
    return Account.objects.filter(is_active=True, is_staff=False)

@register.assignment_tag
def all_projects():
    return Project.objects.filter(status=True)

@register.simple_tag
def check_attendance(value):
    date_today = datetime.now()
    this_time = datetime.strftime(date_today, '%H:%m')
    if this_time > '10:00':
        return 'red'
