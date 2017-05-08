
from django.db import models
from accounts.models import Account


class Projects(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    hours = models.FloatField()
    hours_spent = models.FloatField(default=0)


    class Meta:
        verbose_name_plural = "project"


    def __str__(self):
        return self.name


class WorkDiary(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    hours = models.FloatField()
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "workdiary"


    def __str__(self):
        return self.description