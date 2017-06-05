from django import template
from accounts.models import Account
from projects.models import Project

register = template.Library()


@register.inclusion_tag('management/employees_list.html')
def all_employees():
    return {'employees': Account.objects.filter(is_active=True, is_staff=False)}


@register.inclusion_tag('management/projects_list.html')
def all_projects():
    return {'projects': Project.objects.all()}
