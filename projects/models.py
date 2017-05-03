from django.db import models

# Create your models here.


class Projects(models.Model):

    name = models.CharField(max_length=200)
    date = models.DateField()
    hours = models.TimeField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return self.name