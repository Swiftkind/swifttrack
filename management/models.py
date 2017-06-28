from django.db import models
from accounts.models import Account
from django.conf import settings
from datetime import datetime

# Create your models here.


class Requests(models.Model):
    RFL = "RFL"
    EL = "EL"
    OR = "OR"
    TYPES_OF_REQUEST = (
        (RFL, 'Request for leave'),
        (EL, 'Emergency leave'),
        (OR, 'Other request')
    )
    employee = models.ForeignKey(Account)
    subject = models.CharField(max_length=3, choices=TYPES_OF_REQUEST, default=RFL)
    date_requested = models.DateTimeField(auto_now=True)
    date_of_leave = models.DateTimeField(blank=True, null=True)
    date_of_return = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{} : {}".format(self.subject, self.employee)


class Misc(models.Model):
    RECURRING = 'recurring'
    FIXED = 'fixed'
    TYPES = (
        (RECURRING, 'Recurring'),
        (FIXED, 'Fixed'),
    )
    employees = models.ForeignKey(Account)
    name = models.CharField(max_length=200)
    types = models.CharField(max_length=150, choices=TYPES, default=RECURRING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    months  = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Misc"

    def __str__(self):
        return "{} : {}".format(self.name, self.employees)
