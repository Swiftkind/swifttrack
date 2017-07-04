from django import template
from django.utils import timezone
from datetime import datetime, timedelta

from projects.models import WorkDiary

register = template.Library()

@register.simple_tag
def compute_weekly_hours(value):
    week_day = timezone.now().date().weekday()
    start = timezone.now().date() - timedelta(days=week_day)
    end = timezone.now().date() + timedelta(days=4)
    workdiaries = WorkDiary.objects.filter(project_assignment=value, date__range=[start, end]).values_list('hours', flat=True)
    return sum(workdiaries)
