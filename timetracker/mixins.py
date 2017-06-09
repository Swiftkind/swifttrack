import datetime

from django.utils import timezone

from timetracker.models import TaskLog


class TimeSheetMixin(object):
    """Manage time sheet
    """

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

        logs = TaskLog.objects.filter(task__member__employee=user)

        if project:
            logs = logs.filter(task__member__project=project)

        return logs

    def weekly_hours(self, user, project):
        """Check hours for the week
        """

        week_dates = self.week_date()
        tasklogs = self.user_timesheet(user, project).filter(start__range=[week_dates['start_date'], week_dates['current_date']])
        return self.total_hours(tasklogs)