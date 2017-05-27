import datetime

from django.utils import timezone

from project.models import Project, ProjectAssignment
from timetracker.models import TaskLog


class TimeSheetMixin(object):
    """Manage time sheet
    """

    def user_projects(self, user):
        """List user projects
        """
        projects =ProjectAssignment.objects.filter(account=user)
        return Project.objects.filter(id__in=projects.values_list('project__id', flat=True))

    def total_hours(self, queryset):
        """Get total hours
        """
        seconds = 0
        for log in queryset:
            seconds += log.seconds

        return str(datetime.timedelta(seconds=seconds))

    def week_date(self):
        """We the range date for the week
        """
        date = timezone.now().today()
        current_date = date
        monday = date - datetime.timedelta(days=date.weekday())
        return {
            'start_date': monday.date(),
            'current_date': current_date
        }

    def user_timesheet(self, user, project=None):
        """Check user timesheet
        """

        logs = TaskLog.objects.filter(member__account=user)

        if project:
            logs = logs.filter(member__project=project)

        return logs
