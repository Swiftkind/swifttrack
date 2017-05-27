import datetime

from django.utils import timezone
from django.db import models


class Task(models.Model):
    memo = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    modefied = models.DateTimeField(auto_now=True)
    member = models.ForeignKey('projects.ProjectAssignment')
    mark_as_done = models.BooleanField(default=False)

    @property
    def log(self):
        """Hours spent for the task
        """
        logs = TaskLog.objects.filter(task=self)
        seconds = 0

        for log in logs:
            seconds += log.seconds

        return str(datetime.timedelta(seconds=seconds))

    def time_out(self):
        """Time-out on the task
        """
        logs = TaskLog.objects.filter(task=self, end=None)
        logs.update(end=timezone.now())

    def is_logged(self):
        return TaskLog.objects.filter(task=self, end=None).exists()

    def time_in(self):
        """Time-in on the task
        """
        if self.is_logged():
            self.time_out()
        else:
            TaskLog.objects.create(task=self)

    def __str__(self):
        return self.memo


class TaskLog(models.Model):
    task = models.ForeignKey(Task)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)

    @property
    def seconds(self):
        """Get the difference between start and end
        """
        end = self.end or timezone.now()
        result = end - self.start
        return result.seconds

    @property
    def log(self):
        """Get the time spent for the log
        """
        return str(datetime.timedelta(seconds=self.seconds))

    def __str__(self):
        return self.task.memo
