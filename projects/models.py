
from django.db import models
from accounts.models import Account


class Project(models.Model):

    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "project"


    def __str__(self):
        return "{}".format(self.name)


class ProjectAssignment(models.Model):

    employee = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    weekly_hours = models.FloatField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "project-assignment"


    def __str__(self):
        return "{}".format(self.project.name)


class WorkDiary(models.Model):

    project_assignment = models.ForeignKey(ProjectAssignment, null=True, on_delete=models.CASCADE)
    finished_task = models.TextField()
    todo_task = models.TextField()
    issues = models.TextField()
    date = models.DateTimeField(auto_now=True)
    hours = models.FloatField()


    class Meta:
        verbose_name_plural = "workdiary"


    def __str__(self):
        return "{}".format(self.id)