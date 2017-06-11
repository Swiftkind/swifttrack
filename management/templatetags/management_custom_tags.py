from django import template
from accounts.models import Account
from projects.models import Project

register = template.Library()

@register.assignment_tag
def all_employees():
    return Account.objects.filter(is_active=True, is_staff=False)

@register.assignment_tag
def all_projects():
    return Project.objects.all()